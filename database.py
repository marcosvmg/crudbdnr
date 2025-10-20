import redis
from datetime import datetime

# Conecta-se ao Redis. O 'decode_responses=True' é crucial para que
# as respostas do Redis venham como strings e não como bytes.
try:
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    r.ping()
    print("Conexão com o Redis estabelecida com sucesso.")
except redis.exceptions.ConnectionError as e:
    print(f"Não foi possível conectar ao Redis: {e}")
    exit()

def criar_tarefa(titulo, descricao):
    """
    Cria uma nova tarefa no Redis.
    Utiliza um contador atômico para garantir IDs únicos.
    """
    try:
        # Gera um novo ID único para a tarefa usando um contador no Redis
        id_tarefa = r.incr('contador_id_tarefa')
        chave = f'tarefa:{id_tarefa}'
        
        tarefa = {
            'titulo': titulo,
            'descricao': descricao,
            'data_criacao': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            'status': 'Pendente'
        }
        
        # Armazena a tarefa como um hash no Redis
        r.hset(chave, mapping=tarefa)
        return id_tarefa
    except Exception as e:
        print(f"Erro ao criar tarefa: {e}")
        return None

def listar_todas_tarefas():
    """
    Retorna uma lista de todas as tarefas armazenadas no Redis.
    """
    try:
        chaves_tarefas = r.keys('tarefa:*')
        tarefas = []
        for chave in chaves_tarefas:
            id_tarefa = chave.split(':')[-1]
            tarefa = r.hgetall(chave)
            tarefa['id'] = id_tarefa
            tarefas.append(tarefa)
        # Ordena as tarefas pelo ID de forma decrescente para mostrar as mais novas primeiro
        return sorted(tarefas, key=lambda x: int(x['id']), reverse=True)
    except Exception as e:
        print(f"Erro ao listar tarefas: {e}")
        return []

def obter_tarefa(id_tarefa):
    """
    Obtém uma única tarefa pelo seu ID.
    """
    try:
        chave = f'tarefa:{id_tarefa}'
        tarefa = r.hgetall(chave)
        if tarefa:
            tarefa['id'] = id_tarefa
        return tarefa
    except Exception as e:
        print(f"Erro ao obter tarefa {id_tarefa}: {e}")
        return None

def atualizar_tarefa(id_tarefa, dados_atualizacao):
    """
    Atualiza um ou mais campos de uma tarefa existente.
    'dados_atualizacao' deve ser um dicionário.
    """
    try:
        chave = f'tarefa:{id_tarefa}'
        if r.exists(chave):
            r.hset(chave, mapping=dados_atualizacao)
            return True
        return False
    except Exception as e:
        print(f"Erro ao atualizar tarefa {id_tarefa}: {e}")
        return False

def deletar_tarefa(id_tarefa):
    """
    Exclui uma tarefa do Redis pelo seu ID.
    """
    try:
        chave = f'tarefa:{id_tarefa}'
        if r.exists(chave):
            r.delete(chave)
            return True
        return False
    except Exception as e:
        print(f"Erro ao deletar tarefa {id_tarefa}: {e}")
        return False