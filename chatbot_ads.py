import re
import unicodedata
from difflib import SequenceMatcher


# Base de conhecimento: você pode adicionar mais perguntas e respostas.
FAQ = [
    {
        "perguntas": [
            "o que é ADS",
            "o que significa análise e desenvolvimento de sistemas",
            "qual é o curso de ADS",
        ],
        "resposta": (
            "ADS significa Análise e Desenvolvimento de Sistemas. "
            "É um curso voltado à criação, manutenção e análise de sistemas e softwares."
        ),
    },
    {
        "perguntas": [
            "o que se estuda em ADS",
            "quais matérias tem no curso de ADS",
            "o que vou aprender em ADS",
        ],
        "resposta": (
            "Em ADS, geralmente se estudam programação, banco de dados, engenharia "
            "de software, análise de requisitos, redes, segurança e desenvolvimento web."
        ),
    },
    {
        "perguntas": [
            "preciso saber programar para começar ADS",
            "é necessário saber programação antes do curso",
            "posso fazer ADS sem experiência em programação",
        ],
        "resposta": (
            "Não é obrigatório saber programar antes de começar. O curso costuma "
            "ensinar os fundamentos desde o início, mas praticar por conta própria ajuda."
        ),
    },
    {
        "perguntas": [
            "o que é algoritmo",
            "explique algoritmo",
            "para que serve um algoritmo",
        ],
        "resposta": (
            "Um algoritmo é uma sequência de passos para resolver um problema "
            "ou realizar uma tarefa."
        ),
    },
    {
        "perguntas": [
            "o que é banco de dados",
            "para que serve banco de dados",
            "explique banco de dados",
        ],
        "resposta": (
            "Um banco de dados organiza informações para que possam ser armazenadas, "
            "consultadas e atualizadas. SQL é uma linguagem bastante usada para trabalhar com eles."
        ),
    },
    {
        "perguntas": [
            "qual linguagem de programação devo aprender",
            "qual linguagem é melhor para começar",
            "por onde começar a programar",
        ],
        "resposta": (
            "Python costuma ser uma boa linguagem para começar por ter uma sintaxe "
            "simples. JavaScript também é uma opção, especialmente para desenvolvimento web."
        ),
    },
    {
        "perguntas": [
            "o que é engenharia de software",
            "explique engenharia de software",
            "para que serve engenharia de software",
        ],
        "resposta": (
            "Engenharia de software reúne práticas para planejar, construir, testar "
            "e manter software com qualidade."
        ),
    },
    {
        "perguntas": [
            "o que é levantamento de requisitos",
            "o que são requisitos de um sistema",
            "explique requisitos de software",
        ],
        "resposta": (
            "Requisitos descrevem o que um sistema deve fazer e as condições que "
            "ele precisa atender. Eles ajudam a equipe a entender o problema antes de programar."
        ),
    },
    {
        "perguntas": [
            "o que é git",
            "para que serve o git",
            "explique controle de versão",
        ],
        "resposta": (
            "Git é uma ferramenta de controle de versão. Ela registra alterações no código "
            "e facilita o trabalho colaborativo entre pessoas desenvolvedoras."
        ),
    },
]


def normalizar(texto):
    """Deixa o texto em minúsculas e remove acentos e pontuação."""
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(
        caractere for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )
    return re.sub(r"[^a-z0-9\s]", " ", texto).strip()


def similaridade(pergunta, exemplo):
    """Combina semelhança de texto e palavras em comum."""
    pergunta_norm = normalizar(pergunta)
    exemplo_norm = normalizar(exemplo)

    palavras_pergunta = set(pergunta_norm.split())
    palavras_exemplo = set(exemplo_norm.split())

    if not palavras_pergunta or not palavras_exemplo:
        return 0.0

    intersecao = palavras_pergunta & palavras_exemplo
    jaccard = len(intersecao) / len(palavras_pergunta | palavras_exemplo)
    texto = SequenceMatcher(None, pergunta_norm, exemplo_norm).ratio()

    return max(jaccard, texto)


def responder(pergunta):
    melhor_resposta = None
    melhor_nota = 0.0

    for item in FAQ:
        for exemplo in item["perguntas"]:
            nota = similaridade(pergunta, exemplo)
            if nota > melhor_nota:
                melhor_nota = nota
                melhor_resposta = item["resposta"]

    # Evita escolher uma resposta quando a pergunta não parece relacionada.
    if melhor_nota < 0.20:
        return (
            "Ainda não sei responder isso. Tente perguntar sobre programação, "
            "algoritmos, banco de dados ou matérias de ADS."
        )

    return melhor_resposta


def conversar():
    print("Chatbot de ADS — digite 'sair' para encerrar.")

    while True:
        pergunta = input("\nVocê: ").strip()

        if normalizar(pergunta) in {"sair", "tchau", "encerrar"}:
            print("Bot: Até mais!")
            break

        print("Bot:", responder(pergunta))


if __name__ == "__main__":
    conversar()
