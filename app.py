import streamlit as st
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageEnhance
import io

# --- Configuração da Página ---
st.set_page_config(
    page_title="IROBOT",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("Vendo o invisível - Projeto de inovação I'Robot")
st.write("Este é um protótipo de como funciona nosso projeto de acessibilidade em mapas virtuais.")

# --- Barra Lateral (Parâmetros) ---
st.sidebar.header("Configurações")

# 1. Parâmetros de Cor (K-Means e Saturação)
# Mantivemos a saturação pois ela ajuda o K-Means a separar melhor as cores
SATURATION_FACTOR = st.sidebar.slider("Reforço de Cor (Pré-processamento)", 1.0, 5.0, 2.0, 0.1)

# N_CORES substitui o antigo nível de posterização. 
# O código do Corel sugeria 93, mas deixamos ajustável.
N_CLUSTERS = st.sidebar.slider("Quantidade de Cores (K-Means)", 2, 64, 16, 1)

# Suavização (Median Blur) - Remove ruídos e deixa a cor "chapada"
# O slider garante números ímpares (obrigatório para o OpenCV)
BLUR_INTENSITY = st.sidebar.slider("Suavização das Manchas", 1, 15, 7, 2)

# 2. Parâmetros Geométricos
STEP_SIZE = st.sidebar.slider("Tamanho do Bloco (Pixels)", 5, 50, 50, 1)
MIN_SIZE_PERCENT = st.sidebar.slider("Tamanho Mínimo Visível (%)", 0, 20, 5, 1) / 100.0

st.sidebar.subheader("Aparência das Formas")
outline_choice = st.sidebar.radio("Cor do Contorno das Formas", ["Preto", "Branco"], index=0)

OPACITY_VAL = int(255 * 0.60)

if outline_choice == "Preto":
    SHAPE_COLOR = (0, 0, 0, OPACITY_VAL) 
else:
    SHAPE_COLOR = (255, 255, 255, OPACITY_VAL) 

LINE_WIDTH = 1

st.sidebar.subheader("Filtros de Fundo")
BLACK_THRESHOLD = st.sidebar.slider("Ignorar pixels muito escuros", 0, 100, 10)

# --- Funções de Desenho ---
def draw_triangle(draw, center_x, center_y, size, outline_color):
    s = size / 2
    points = [
        (center_x, center_y - s),      
        (center_x - s, center_y + s),  
        (center_x + s, center_y + s)   
    ]
    draw.polygon(points, outline=outline_color, width=LINE_WIDTH)

def draw_square(draw, center_x, center_y, size, outline_color):
    s = size / 2
    draw.rectangle(
        (center_x - s, center_y - s, center_x + s, center_y + s),
        outline=outline_color,
        width=LINE_WIDTH
    )

def draw_circle(draw, center_x, center_y, size, outline_color):
    s = size / 2
    draw.ellipse(
        (center_x - s, center_y - s, center_x + s, center_y + s),
        outline=outline_color,
        width=LINE_WIDTH
    )

# --- Nova Lógica de Processamento (Baseada no seu script Python) ---
def apply_kmeans_processing(pil_img, n_colors, blur_k, saturation):
    # 1. Conversão PIL -> OpenCV
    # Convertemos para numpy array
    img_np = np.array(pil_img)
    
    # 2. Pré-processamento: Saturação (Ajuda o K-Means a separar cores vivas)
    if saturation != 1.0:
        # Convertemos para PIL rapidinho para usar o Enhancer que é ótimo, depois voltamos
        temp_pil = Image.fromarray(img_np)
        enhancer = ImageEnhance.Color(temp_pil)
        img_np = np.array(enhancer.enhance(saturation))

    # O OpenCV trabalha com BGR por padrão se lido via cv2.imread, 
    # mas como viemos do PIL, já estamos em RGB. Mantemos RGB.
    
    # 3. Formatar dados para o algoritmo K-Means
    # Reshape para uma lista de pixels (altura*largura, 3 canais)
    Z = img_np.reshape((-1, 3))
    Z = np.float32(Z)

    # 4. Executar K-Means (Configuração do seu script)
    # criteria: (type, max_iter, epsilon)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    
    # KMEANS_PP_CENTERS ajuda a escolher centros iniciais melhores
    ret, label, center = cv2.kmeans(Z, n_colors, None, criteria, 3, cv2.KMEANS_PP_CENTERS)

    # 5. Reconstruir a imagem
    center = np.uint8(center)
    res = center[label.flatten()]
    img_quantized = res.reshape((img_np.shape))

    # 6. Aplicar Suavização (Median Blur)
    # Isso cria o efeito "blob" (manchas sólidas) removendo ruído
    if blur_k > 0:
        # Garante que seja ímpar e >= 1
        k_size = blur_k if blur_k % 2 != 0 else blur_k + 1
        img_final = cv2.medianBlur(img_quantized, k_size)
    else:
        img_final = img_quantized

    # Retorna como imagem PIL para o resto do app usar
    return Image.fromarray(img_final)

# --- Lógica Principal do App ---
def process_image(original_img):
    orig_w, orig_h = original_img.size
    
    # --- 1. Aplica o efeito K-Means (O "PowerTRACE" do código enviado) ---
    # Isso substitui a antiga saturação/posterização
    img_analysis_final = apply_kmeans_processing(
        original_img, 
        n_colors=N_CLUSTERS, 
        blur_k=BLUR_INTENSITY,
        saturation=SATURATION_FACTOR
    )
    
    # --- 2. Camada de Desenho (Geometria) ---
    shape_layer = Image.new('RGBA', (orig_w, orig_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(shape_layer)
    
    progress_bar = st.progress(0)
    total_steps = (orig_h // STEP_SIZE)
    if total_steps == 0: total_steps = 1

    # Convertemos para numpy para leitura rápida dos blocos
    img_analysis_arr = np.array(img_analysis_final)

    for i, y in enumerate(range(0, orig_h, STEP_SIZE)):
        progress_val = i / total_steps
        if progress_val > 1.0: progress_val = 1.0
        progress_bar.progress(progress_val)
        
        for x in range(0, orig_w, STEP_SIZE):
            # Define limites do bloco (tratando bordas)
            x_end = min(x + STEP_SIZE, orig_w)
            y_end = min(y + STEP_SIZE, orig_h)
            
            # Recorta bloco do array numpy
            block = img_analysis_arr[y:y_end, x:x_end]
            
            if block.size == 0: continue
            
            # Média de cor do bloco processado pelo K-Means
            avg_color = np.mean(block, axis=(0, 1))
            
            if len(avg_color) >= 3:
                r, g, b = avg_color[0], avg_color[1], avg_color[2]
            else:
                continue 

            intensity = (r + g + b) / 3
            if intensity < BLACK_THRESHOLD:
                continue

            center_x = x + (STEP_SIZE / 2)
            center_y = y + (STEP_SIZE / 2)
            
            # Proporções (0-255 -> 0.0-1.0)
            prop_r = r / 255.0
            prop_g = g / 255.0
            prop_b = b / 255.0
            
            max_size = STEP_SIZE * 0.95
            
            size_r = max_size * prop_r
            size_g = max_size * prop_g
            size_b = max_size * prop_b

            if prop_r > MIN_SIZE_PERCENT:
                draw_triangle(draw, center_x, center_y, size_r, SHAPE_COLOR)

            if prop_g > MIN_SIZE_PERCENT:
                draw_square(draw, center_x, center_y, size_g, SHAPE_COLOR)

            if prop_b > MIN_SIZE_PERCENT:
                draw_circle(draw, center_x, center_y, size_b, SHAPE_COLOR)
                
    progress_bar.empty()
    
    # 3. Composições finais
    # Debug: Mostra a imagem tratada pelo K-Means com as formas
    img_analysis_rgba = img_analysis_final.convert('RGBA')
    debug_composite = Image.alpha_composite(img_analysis_rgba, shape_layer)
    
    # Final: Mostra a imagem ORIGINAL com as formas
    original_rgba = original_img.convert('RGBA')
    final_composite = Image.alpha_composite(original_rgba, shape_layer)
    
    return img_analysis_final, debug_composite, final_composite

# --- Interface de Upload ---
uploaded_file = st.file_uploader("Escolha uma imagem (JPG, PNG)", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    original_image = Image.open(uploaded_file)
    
    # --- PRÉ-VISUALIZAÇÃO E LEGENDA ---
    st.write("### Pré-visualização")
    
    col_preview, col_legend = st.columns([1, 1.5]) 
    
    with col_preview:
        st.image(original_image, caption="Imagem Original", use_container_width=True)
        
    with col_legend:
        st.markdown("""
        <div style="background-color: #262730; padding: 15px; border-radius: 10px; border: 1px solid #4e4e4e;">
            <h4 style="margin-top: 0;">Legenda Tátil Visual</h4>
            <p style="font-size: 14px; margin-bottom: 10px;">O tamanho da forma indica a intensidade da cor:</p>
            <ul style="list-style-type: none; padding-left: 0;">
                <li style="margin-bottom: 8px;">
                    <span style="font-size: 1.2em;">🔺</span> 
                    <strong style="color: #FF4B4B;">Triângulo</strong> = Intensidade de <b>Vermelho</b>
                </li>
                <li style="margin-bottom: 8px;">
                    <span style="font-size: 1.2em;">🟩</span> 
                    <strong style="color: #3DD56D;">Quadrado</strong> = Intensidade de <b>Verde</b>
                </li>
                <li style="margin-bottom: 8px;">
                    <span style="font-size: 1.2em;">🔵</span> 
                    <strong style="color: #4da6ff;">Círculo</strong> = Intensidade de <b>Azul</b>
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Botão de processamento
    st.write("") 
    if st.button("Processar Imagem (K-Means)", type="primary"):
        with st.spinner('Aplicando K-Means e gerando geometria...'):
            img_kmeans, img_kmeans_shapes, result_img = process_image(original_image)
            
            with st.expander("Processamento Detalhado (Clique para expandir)", expanded=True):
                st.write("Etapas de interpretação do algoritmo:")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.image(original_image, caption="1. Original", use_container_width=True)
                
                with col2:
                    st.image(img_kmeans, caption="2. K-Means (Separação de Cores)", use_container_width=True)
                
                with col3:
                    st.image(img_kmeans_shapes, caption="3. Mapeamento Proporcional", use_container_width=True)

            st.divider()

            st.subheader("Resultado Final")
            st.image(result_img, caption="Imagem Final (Tamanho da forma = Quantidade de Cor)", use_container_width=True)
            
            buf = io.BytesIO()
            result_img.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            st.download_button(
                label="Baixar Resultado Final",
                data=byte_im,
                file_name="acessibilidade_visual_kmeans.png",
                mime="image/png"
            )