# 🤖 Vendo o Invisível - Projeto de Acessibilidade I'Robot

## 📋 Sobre o Projeto

"Vendo o Invisível" é uma solução inovadora de acessibilidade desenvolvida pela equipe i'Robot para o **FIRST LEGO League 2025**. O projeto busca transformar imagens em representações geométricas coloridas, permitindo que arqueólogos com daltonismo visualizem mapas virtuais com total clareza.

A aplicação converte cores RGB complexas em formas geométricas simples e distintas:
- 🔴 **Vermelhos** → Quadrados
- 🟢 **Verdes** → Círculos  
- 🔵 **Azuis** → Triângulos

## 🎯 Objetivo

Aumentar a acessibilidade de mapas virtuais e imagens para pessoas com daltonismo, utilizando representações geométricas que são universalmente reconhecíveis, independentemente da percepção de cor.

## ✨ Funcionalidades

- ✅ Upload de imagens JPG e PNG
- ✅ Processamento com super saturação de cores
- ✅ Conversão de cores em formas geométricas
- ✅ Interface intuitiva com configurações ajustáveis
- ✅ Visualização em tempo real antes e depois
- ✅ Download da imagem processada em PNG

## ⚙️ Configurações Personalizáveis

A aplicação oferece controles interativos na barra lateral:

| Parâmetro | Range | Padrão | Descrição |
|-----------|-------|--------|-----------|
| **Fator de Saturação** | 1.0 - 10.0 | 5.0 | Intensidade da saturação de cores |
| **Tamanho do Bloco** | 5 - 50px | 10px | Tamanho de cada bloco processado |
| **Limiar de Presença** | 0.1 - 0.9 | 0.2 | Sensibilidade de detecção de cor |
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
2. ⚙️ Ajuste os parâmetros na barra lateral conforme necessário
3. ▶️ Clique em "Processar Imagem"
4. 👀 Veja as três versões lado a lado:
   - Imagem original
   - Imagem saturada
   - Resultado com formas geométricas
5. 💾 Baixe a imagem processada

## 📦 Dependências

- **streamlit** - Framework para criar aplicações web
- **Pillow (PIL)** - Processamento de imagens
- **numpy** - Operações numéricas

## 🏗️ Arquitetura do Código

### Funções Principais

- **`draw_square()`** - Desenha quadrados vermelhos (dominância de R)
- **`draw_circle()`** - Desenha círculos verdes (dominância de G)
- **`draw_triangle()`** - Desenha triângulos azuis (dominância de B)
- **`process_image()`** - Processa a imagem aplicando saturação e conversão geométrica

### Fluxo de Processamento

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
