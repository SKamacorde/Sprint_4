class Produto:
    def __init__(self, cd_produto, nm_produto, cd_status, cd_usuario_inclusao, dt_inclusao, cd_usuario_alteracao, dt_alteracao):
        self.cd_produto = cd_produto
        self.nm_produto = nm_produto
        self.cd_status = cd_status
        self.cd_usuario_inclusao = cd_usuario_inclusao
        self.dt_inclusao = dt_inclusao
        self.cd_usuario_alteracao = cd_usuario_alteracao
        self.dt_alteracao = dt_alteracao

    def __repr__(self):
        return f"<Produto(cd_produto={self.cd_produto}, nm_produto='{self.nm_produto}', cd_status={self.cd_status})>"