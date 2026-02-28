# Organizador de Arquivos Minimalista 🗂️✨

Este projeto é uma **ferramenta para organização automática de arquivos**, feita em Python, que classifica arquivos por tipo e subpasta, com foco em eficiência e minimalismo.

## Estrutura do projeto

- `maestro.py` – Primeira versão funcional (v1.0) do organizador de arquivos.  
- `maestro-eficiente.py` – Versão otimizada do `maestro.py`, com código minimalista, variáveis de 1 caractere em chinês e maior eficiência no binário.  
- `cria-muito-arquivo.py` / `cria-pouco-arquivo.py` – Scripts auxiliares para gerar arquivos de teste.

## Objetivo do projeto

- Organizar arquivos automaticamente em diretórios categorizados.  
- Tornar o código **leve, minimalista e eficiente** no binário.  
- Experimentar o uso de **caracteres chineses como variáveis**, mantendo legibilidade para humanos e compactação para máquina.

## **Como usar**

```bash
python maestro-eficiente.py -o /caminho/origem -d /caminho/destino -r /caminho/relatório.csv [opções]
```

### **Argumentos obrigatórios**

* `-o, --origem` : Diretório raiz de origem dos arquivos.
* `-d, --destino` : Diretório onde os arquivos serão organizados.

### **Opções**

* `-r, --report` : Caminho para gerar um relatório CSV com as ações realizadas (`origem`, `destino`, `ação`).
* `-c, --copia` : Copiar os arquivos ao invés de movê-los.
* `--dry-run` : Simular a operação sem mover ou copiar arquivos (apenas mostra o que seria feito).

---

Divirta-se organizando seus arquivos! 🚀