import json


class MensagemProtocolo:
    def __init__(self, mensagem):
        self.__mensagem = mensagem
    

    def encode_menssagem(self):
        return json.dumps(self.__mensagem).encode("utf-8")
    

    def decode_menssagem(self, mensagem):
        return json.loads(mensagem.decode("utf-8"))
    


class MensagemSolicitarDescarteCartaJogador(MensagemProtocolo):
    def __init__(self, id):
        super().__init__({"Tipo": "Solicitação",
                          "Ação": "Obter carta descartada",
                          "IdJogador": id})
        

class MensagemRespostaDescarteCartaJogador(MensagemProtocolo):
    def __init__(self, carta):
        super().__init__({"Tipo": "Resposta",
                          "CartaDescartada": carta})
        

class MensagemSocilitarEntrarFila(MensagemProtocolo):
    def __init__(self):
        super().__init__({"Tipo": "Solicitação",
                         "Ação": "Entrar na fila"})
        
