from psycopg2 import connect
# noinspection PyProtectedMember
from psycopg2._psycopg import connection
import os
from env_pomes import APP_PREFIX, env_get_int, env_get_str

# dados para acesso ao BD
DB_HOST: str = env_get_str(f"{APP_PREFIX}_DB_HOST")
DB_PORT: int = env_get_int(f"{APP_PREFIX}_DB_PORT")
DB_NAME: str = os.environ[f"{APP_PREFIX}_DB_NAME"]
DB_USER: str = os.environ[f"{APP_PREFIX}_DB_USER"]
DB_PWD: str = os.environ[f"{APP_PREFIX}_DB_PWD"]


def db_connect(errors: list[str]) -> connection:
    """
    Obtem e retorna uma conexão ao banco de dados, ou *None* se a conexão não pode ser obtida.

    :param errors: lista a ser apensada com mensagem apropriada, em caso de erro
    :return: a conexão ao banco de dados
    """
    # inicializa a variável de retorno
    result: connection | None = None

    # obtem a conexão com o BD
    try:
        result = connect(host=DB_HOST,
                         port=DB_PORT,
                         database=DB_NAME,
                         user=DB_USER,
                         password=DB_PWD)
    except Exception as e:
        errors.append(__db_except_msg(e))

    return result


def db_exists(errors: list[str], table: str, where_attrs: list[str], where_vals: tuple) -> bool:
    """
    Determina se a tabela *table* no banco de dados contem pelo menos uma tupla onde *attrs* são iguais a
    *values*, respectivamente. Se mais de um, os atributos são concatenados pelo conector lógico *AND*.
    Retorna *None* se houver erro na consulta ao banco de dados.

    :param errors: lista a ser apensada com mensagem apropriada, em caso de erro
    :param table: a tabela a ser pesquisada
    :param where_attrs: os atributos para a busca
    :param where_vals: lista de valores a serem atribuídos aos atributos
    :return: True se não houve erro, e se pelo menos uma tupla existir
    """
    sel_stmt: str = f"SELECT * FROM {table}" # noqa
    if len(where_attrs) > 0:
        sel_stmt += " WHERE " + "".join(f"{attr} = %s AND " for attr in where_attrs)[0:-5]
    rec: tuple = db_select_one(errors, sel_stmt, where_vals)
    result: bool = None if len(errors) > 0 else rec is not None

    return result


def db_select_one(errors: list[str], sel_stmt: str,
                  where_vals: tuple, required: bool = False) -> tuple:
    """
    Busca no banco de dados e retorna a primeira tupla que satisfaça o comando de busca *sel_stmt*.
    O comando pode opcionalmente conter critérios de busca, com valores respectivos fornecidos
    em *where_vals*. A lista de valores para um atributo com a cláusula *IN* deve estar contida
    em tupla específica. Na hipóteese de erro, ou se a busca resultar vazia, *None* é retornado.

    :param errors: lista a ser apensada com mensagem apropriada, em caso de erro
    :param sel_stmt: comando SELECT para a busca
    :param where_vals: lista de valores a serem associados aos critérios de busca
    :param required: define se busca vazia deve ser considerada erro
    :return: tupla contendo o resultado da busca, ou None se houve erro ou se a busca resultar vazia
    """
    # inicializa a variável de retorno
    result: tuple | None = None

    exc: bool = False
    try:
        with connect(host=DB_HOST,
                     port=DB_PORT,
                     database=DB_NAME,
                     user=DB_USER,
                     password=DB_PWD) as conn:
            # obtem o cursor e executa a operação
            with conn.cursor() as cursor:
                sel_stmt += " LIMIT 1"
                cursor.execute(query=f"{sel_stmt};",
                               vars=where_vals)
                # obtem a primeira tupla retornada pelo SELECT (None se nenhuma foi retornada)
                result = cursor.fetchone()
    except Exception as e:
        exc = True
        errors.append(__db_except_msg(e))

    # o parâmetro 'required' foi definido e nenhum registro foi obtido ?
    if required and not exc and result is None:
        # sim, reporte o erro
        errors.append(__db_required_msg(sel_stmt, where_vals))

    return result


def db_select_all(errors: list[str], sel_stmt: str,
                  where_vals: tuple, required: bool = False) -> list[tuple]:
    """
    Busca no banco de dados e retorna todas as tuplas que satifaçam o comando de busca *sele_stmt*.
    O comando pode opcionalmente conter critérios de busca, com valores respectivos fornecidos
    em *where_vals*. A lista de valores para um atributo com a cláusula *IN* deve estar contida
    em tupla específica. Se a busca resultar vazia, uma lista vazia é retornado.

    :param errors: lista a ser apensada com mensagem apropriada, em caso de erro
    :param sel_stmt: comando SELECT para a busca
    :param where_vals: lista de valores a serem associados aos critérios de busca
    :param required: define se busca vazia deve ser considerada erro
    :return: lista de tuplas contendo o resultado da busca, ou []  se a busca resultar vazia
    """
    # inicializa a variável de retorno
    result: list[tuple] = []

    exc: bool = False
    try:
        with connect(host=DB_HOST,
                     port=DB_PORT,
                     database=DB_NAME,
                     user=DB_USER,
                     password=DB_PWD) as conn:
            # obtem o cursor e executa a operação
            with conn.cursor() as cursor:
                cursor.execute(query=f"{sel_stmt};",
                               vars=where_vals)
                # obtem as tuplas retornadas
                for record in cursor:
                    result.append(record)
    except Exception as e:
        exc = True
        errors.append(__db_except_msg(e))

    # o parâmetro 'required' foi definido, não houve erros, e nenhum registro foi obtido ?
    if required and not exc and len(result) == 0:
        # sim, reporte o erro
        errors.append(__db_required_msg(sel_stmt, where_vals))

    return result


def db_insert(errors: list[str], insert_stmt: str, insert_vals: tuple) -> int:
    """
    Insere no banco de dados uma tupla com valores definidos em *insert_vals*.

    :param errors: lista a ser apensada com mensagem apropriada, em caso de erro
    :param insert_stmt: comando INSERT
    :param insert_vals: lista de valores a serem inseridos
    :return: o número de tuplas inseridas (0 ou 1), ou None em caso de erro
    """
    return __db_modify(errors, insert_stmt, insert_vals)


def db_update(errors: list[str], update_stmt: str,
              update_vals: tuple, where_vals: tuple) -> int:
    """
    Atualiza uma ou mais tuplas no banco de dados, segundo as definições do comando
    *update_stmt*. Os valores para essa atualização estão em *update_vals*.
    Os valores para a seleção das tuplas a serem atualizadas estão em *where_vals*.

    :param errors: lista a ser apensada com mensagem apropriada, em caso de erro
    :param update_stmt: comando UPDATE
    :param update_vals: lista de valores para a atualização
    :param where_vals: lista de valores para os critérios de seleção de tuplas
    :return: o número de tuplas atualizadas
    """
    values: tuple = update_vals + where_vals
    return __db_modify(errors, update_stmt, values)


def db_delete(errors: list[str], delete_stmt: str, where_vals: tuple) -> int:
    """
    Exclui uma ou mais tuplas no banco de dados, segundo as definições do comando *delete_stmt*.
    Os valores para a seleção das tuplas a serem excuídas estão em *where_vals*.

    :param errors: lista a ser apensada com mensagem apropriada, em caso de erro
    :param delete_stmt: comando DELETE
    :param where_vals: lista de valores para os critérios de seleção de tuplas
    :return: o número de tuplas excluídas
    """
    return __db_modify(errors, delete_stmt, where_vals)


# modifica tabela no banco de dados e retorna o número de tuplas afetadas
def __db_modify(errors: list[str], modify_stmt: str, bind_vals: tuple) -> int:
    """
    Modifica o banco de dados, inserindo, atualizando ou excluindo tuplas, segundo as
    definições do comando *modify_stmt*. Os valores para essa modificação, seguidos dos
    valores para a seleção das tuplas, estão em *bind_vals*.

    :param errors: lista a ser apensada com mensagem apropriada, em caso de erro
    :param modify_stmt: comando INSERT, UPDATE ou DELETE
    :param bind_vals: lista de valores para modificação e seleção de tuplas
    :return: o número de tuplas inseridas, atualizadas ou excluídas, ou None em caso de erro
    """
    result: int | None = None

    try:
        with connect(host=DB_HOST,
                     port=DB_PORT,
                     database=DB_NAME,
                     user=DB_USER,
                     password=DB_PWD) as conn:
            # obtem o sursor e executa a operação
            with conn.cursor() as cursor:
                cursor.execute(query=f"{modify_stmt};",
                               vars=bind_vals)
                result = cursor.rowcount
                conn.commit()
    except Exception as e:
        errors.append(__db_except_msg(e))

    return result


def __db_except_msg(exception: Exception) -> str:
    """
    Formata e retorna a mensagem de erro correspondente à exceção levantada no acesso
    ao banco de dados.

    :param exception: a exceção levantada
    :return: A mensagem de erro formatada
    """
    exc_msg: str = f"{exception}"
    pos: int = exc_msg.find("LINE 1")
    if pos > 0:
        exc_msg = exc_msg[:pos]
    if hasattr(exception, "cursor") and hasattr(exception.cursor, "query"):
        query: str = exception.cursor.query.decode()
        exc_msg += f" ({query})"

    exc_msg = exc_msg.replace('"', "'") \
                     .replace('\n', " ") \
                     .replace('\t', " ") \
                     .replace("\\", "")
    result = f"Error accessing {DB_NAME} at {DB_HOST}: {exc_msg}"

    return result


def __db_required_msg(sel_stmt: str, where_vals: tuple) -> str:
    """
    Formata e retorna a mensagem indicativa de busca vazia.

    :param sel_stmt: o comando de busca utilizado
    :param where_vals: a lista de valores constituindo os critérios de busca
    :return: mensagem indicativa de busca vazia
    """
    stmt: str = sel_stmt.replace('"', "'") \
                        .replace('\n', " ") \
                        .replace('\t', " ") \
                        .replace("\\", "")
    result: str = f"No record found in {DB_NAME} at {DB_HOST}, for {stmt}"

    for val in where_vals:
        if isinstance(val, str):
            val = f"'{val}'"
        else:
            val = str(val)
        result = result.replace("%s", val, 1)

    return result
