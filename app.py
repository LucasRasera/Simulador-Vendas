import streamlit as st

st.title('Simulador PBO')

VALOR_SALARIO = 1412
TETO_BPO = VALOR_SALARIO*0.7
PESO_VENDA = 0.6
PESO_QUALIDADE = 0.1
PESO_LOGADO = 0.1
PESO_PRODUTIVO = 0.2

def pbo_vendas(vendas):
    if vendas < 30:
        meta_atingida = 0
    else:
        meta_atingida = vendas/60 

    valor_bpo = TETO_BPO * PESO_VENDA
    valor_bpo = valor_bpo * meta_atingida
    return valor_bpo

def pbo_qualidade(qualidade):
    if qualidade < 85:
        meta_atingida = 0
    else:
        meta_atingida = TETO_BPO * PESO_QUALIDADE
    return meta_atingida

def pbo_logado(logado):
    if logado < 93:
        meta_atingida = 0
    else:
        meta_atingida = TETO_BPO * PESO_LOGADO
    return meta_atingida

def pbo_produtivo(produtivo):
    if produtivo < 93:
        meta_atingida = 0
    else:
        meta_atingida = TETO_BPO * PESO_PRODUTIVO
    return meta_atingida

with st.form('simulador'):
    vendas = st.number_input('Quantidade de Vendas')
    qualidade = st.number_input('Média de Qualidade')
    tempo_logado = st.number_input('Tempo Logado')
    tempo_produtivo = st.number_input('Tempo Produtivo')
    ajustes = st.number_input('Ajustes')
    injustificada = st.toggle('Falta injustifcada?')
    justificadas = st.toggle('3 ou mais faltas justificaddas?')

    submitted = st.form_submit_button("Calcular :money_with_wings:")
    if submitted:
        valor_venda = pbo_vendas(vendas)
        valor_qualidade = pbo_qualidade(qualidade)
        valor_logado = pbo_logado(tempo_logado)
        valor_produtivo = pbo_produtivo(tempo_produtivo)
        total = valor_venda + valor_qualidade + valor_logado + valor_produtivo
        deflator = 0
        
        if valor_venda == 0:
            deflator = 1
        if justificadas:
            deflator = deflator + 0.5
        if injustificada:
            total = 1
        if qualidade < 75:
            deflator = deflator + 0.5
        if tempo_produtivo < 85:
            deflator = deflator + 0.5
        if ajustes > 8:
            deflator = deflator + 0.2

        if deflator >= 1:
            total = 0
        elif deflator == 0:
            pass
        else:     
            total = total - (total * deflator)

        if total > TETO_BPO:
            total = TETO_BPO
        
        st.title(f'R$ {round(total,2)} :money_mouth_face:')
        

