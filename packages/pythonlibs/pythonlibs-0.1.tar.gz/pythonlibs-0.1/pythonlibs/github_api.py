import requests


def buscar_avatar(usuario):
    """
    Busca o link do avatar de um usuário do Github
    :param usuario: string com o nome do usuário desejado
    :return: string com o endereço web da foto do avatar do usuário
    """

    url = f'https://api.github.com/users/{usuario}'

    resp = requests.get(url)
    return resp.json()['avatar_url']


if __name__ == '__main__':
    print(buscar_avatar('michel4lves'))
