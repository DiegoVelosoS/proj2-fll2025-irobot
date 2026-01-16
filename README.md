# 🤖 Vendo o Invisível - Projeto de Acessibilidade I'Robot

## 📋 Sobre o Projeto

"Vendo o Invisível" é uma solução inovadora de acessibilidade desenvolvida pela equipe i'Robot para o **FIRST LEGO League 2025**. O projeto busca transformar imagens em representações geométricas coloridas, permitindo que arqueólogos com daltonismo visualizem mapas virtuais com total clareza.

A aplicação utiliza **K-Means clustering** para segmentar cores e converte a intensidade RGB em formas geométricas proporcionais:
- 🔺 **Vermelho** → Triângulos (tamanho proporcional à intensidade de R)
- 🟩 **Verde** → Quadrados (tamanho proporcional à intensidade de G)
- 🔵 **Azul** → Círculos (tamanho proporcional à intensidade de B)

## 🎯 Objetivo

Aumentar a acessibilidade de mapas virtuais e imagens para pessoas com daltonismo, utilizando representações geométricas que são universalmente reconhecíveis, independentemente da percepção de cor.

## ✨ Funcionalidades

- ✅ Upload de imagens JPG e PNG
- ✅ **K-Means Clustering** para segmentação inteligente de cores
- ✅ **Median Blur** para suavização de manchas de cor
- ✅ Conversão de cores em formas geométricas proporcionais
- ✅ Interface intuitiva com configurações ajustáveis em tempo real
- ✅ Visualização detalhada com 3 etapas de processamento
- ✅ Legenda tátil-visual interativa
- ✅ Download da imagem processada em PNG
- ✅ Deploy pronto para Streamlit Cloud

## ⚙️ Configurações Personalizáveis
### Pré-processamento (K-Means)
| Parâmetro | Range | Padrão | Descrição |
|-----------|-------|--------|-----------|
| **Reforço de Cor (Pré-processamento)** | 1.0 - 5.0 | 2.0 | Intensidade da saturação antes do K-Means |
| **Quantidade de Cores (K-Means)** | 2 - 64 | 16 | Número de cores centrais após agrupamento |
| **Suavização das Manchas** | 1 - 15 | 7 | Kernel de Median Blur para suavizar bordes |

### Geometria e Visualização
| Parâmetro | Range | Padrão | Descrição |
|-----------|-------|--------|-----------|
| **Tamanho do Bloco (Pixels)** | 5 - 50px | 50px | Tamanho de cada bloco analisado |
| **Tamanho Mínimo Visível (%)** | 0 - 20% | 5% | Intensidade mínima para desenhar forma |
| **Cor do Contorno das Formas** | Preto/Branco | Preto | Cor do traço das formas geométricas |

### Filtros de Fundo
| Parâmetro | Range | Padrão | Descrição |
|-----------|-------|--------|-----------|
| **Ignorar pixels muito escuros** | 0 - 100 | 10 | Intensidade mínima para processar bloco de cor |
| **Limiar Saturação** | 0 - 100 | 25 | Limite para cores cinzas |
| **Limiar Preto** | 0 - 100 | 30 | Limite para cores muito escuras |
| **Limiar Branco** | 150 - 255 | 230 | Limite para cores muito claras |

## 🚀 Como Usar

### Instalação

```bash
# Clone o repositório
git clone <seu-repositorio>
cd "Vendo o invisível (App)"

# Instale as dependências
pip install -r requirements.txt
```

### Executar a Aplicação

```bash
streamlit run app.py
```

A aplicação abrirá no navegador padrão em `http://localhost:8501`

### Uso

1. 📤 Faça upload de uma imagem (JPG ou PNG)
2. ⚙️ Ajuste os (≥1.28.0) - Framework para criar aplicações web interativas
- **opencv-python** (≥4.8.0) - Processamento de imagens com K-Means
- **Pillow (PIL)** (≥10.0.0) - Manipulação avançada de imagens
- **numpy** (≥1.24.3) - Operações numéricas e arrays

Instale todas com:
```bash
pip install -r requirements.txt
``` lapply_kmeans_processing()`** - Aplica K-Means, saturação e Median Blur para segmentação de cores
- **`draw_triangle()`** - Desenha triângulo vermelho (proporcional a R)
- **`draw_square()`** - Desenha quadrado verde (proporcional a G)
- **`draw_circle()`** - Desenha círculo azul (proporcional a B)
- **`process_image()`** - Orquestra todo o pipeline de processamento

### Fluxo de Processamento

```
Imagem Original
    ↓
K-Means Clustering (Segmentação de cores)
    ↓
Median Blur (Suavização)
    ↓
Divisão em Blocos
    ↓
Análise de Intensidade RGB por Bloco
    ↓
Desenho Proporcional de Formas
    (tamanho = intensidade da cor)
    ↓
Composição Final (Original + Formas)
```

## 🚀 Deploy no Streamlit Cloud

### Preparação
1. Certifique-se que tem `requirements.txt` atualizado
2. Faça push para um repositório GitHub

### Etapas de Deploy

```bash
# 1. Inicializar Git (se necessário)
git init
git add .
git commit -m "Deploy Vendo o Invisível"

# 2. Fazer push para GitHub
git branch -M main
git push -u origin main
```

3. Acesse [share.streamlit.io](https://share.streamlit.io)
4. Clique em **"New app"**
5. Configure:
   - Repository: `seu-usuario/vendo-o-invisivel`
   - Branch: `main`
   - Main file: `app.py`
6. Clique em **"Deploy"**

A aplicação estará disponível em: `https://seu-usuario-vendo-o-invisivel.streamlit.app/`

## 🎯 Casos de Uso

- 📍 **Arqueologia**: Visualização de mapas com maior clareza para usuários com daltonismo
- 🎓 **Educação**: Ensino de cores e formas para alunos com deficiência visual
- 🏥 **Medicina**: Análise de imagens médicas acessível
- 🎨 **Design**: Teste de acessibilidade de paletas de cores

## 👥 Equipe

**Estande I'Robot** - FIRST LEGO League 2025

## 📝 Licença

Este projeto é desenvolvido para fins educacionais como parte do FIRST LEGO League 2025.

---

**Versão**: 2.0 (K-Means)  
**Última atualização**: 16 de janeiro de 2026 Fluxo de Processamento

```
Imagem Original
    ↓
Conversão RGBA
    ↓
Super Saturação
    ↓
Divisão em Blocos
    ↓
Análise de Cor por Bloco
    ↓
Desenho de Formas Geométricas
    ↓
Imagem Processada com Formas
```

## 👥 Equipe i'Robot

Desenvolvido para o **FIRST LEGO League 2025** com foco em inovação e acessibilidade.

## 🎓 Tecnologias

- Python 3.x
- Streamlit
- PIL/Pillow
- NumPy

## 📸 Exemplo de Uso

Para testar, basta fazer upload de qualquer imagem colorida e ajustar os parâmetros até obter o resultado desejado. A aplicação mostra em tempo real como as configurações afetam o processamento.

## ⚖️ Licença

[Especifique a licença utilizada]

## 📞 Contato

Para mais informações sobre o projeto, visite o estande do i'Robot no FIRST LEGO League 2025!

---

**Desenvolvido com ❤️ pela Equipe i'Robot**
