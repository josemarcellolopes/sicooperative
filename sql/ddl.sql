CREATE TABLE sicooperative.associado (
    id_associado INT AUTO_INCREMENT PRIMARY KEY,
    nome_associado VARCHAR(255) NOT NULL,
    sobrenome_associado VARCHAR(255) NOT NULL,
    idade_associado INT NOT NULL,
    email_associado VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE sicooperative.conta (
    id_conta INT AUTO_INCREMENT PRIMARY KEY,
    tipo_conta ENUM('corrente', 'poupança', 'outro','salário','investimento') NOT NULL,
    data_criacao_conta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_associado INT NOT NULL,
    FOREIGN KEY (id_associado) REFERENCES associado(id_associado)
);

CREATE TABLE sicooperative.cartao (
    id_cartao INT AUTO_INCREMENT PRIMARY KEY,
    numero_cartao BIGINT UNIQUE NOT NULL,
    nome_impresso_cartao VARCHAR(100) NOT NULL,
    id_conta INT NOT NULL,
    FOREIGN KEY (id_conta) REFERENCES conta(id_conta)
);

CREATE TABLE sicooperative.movimento (
    id_movimento INT AUTO_INCREMENT PRIMARY KEY,
    vlr_transacao_movimento DECIMAL(10,2) NOT NULL,
    descricao_transacao_movimento VARCHAR(255) NOT NULL,
    data_movimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_cartao INT NOT NULL,
    FOREIGN KEY (id_cartao) REFERENCES cartao(id_cartao)
);
