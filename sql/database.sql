CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE SCHEMA banco;

CREATE TABLE banco.clientes (
    id SERIAL NOT NULL,
	nome VARCHAR(100) NOT NULL,
	limite INTEGER NOT NULL,
    saldo INTEGER NOT NULL DEFAULT 0,
	created_at TIMESTAMP DEFAULT NOW(),
	updated_at TIMESTAMP NULL,

	CONSTRAINT cliente_pk PRIMARY KEY (id)
);

CREATE TABLE banco.transacoes (
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    cliente_id INTEGER NOT NULL,
    valor INTEGER NOT NULL,
    tipo VARCHAR(1) NOT NULL,
    descricao VARCHAR(10),
    realizada_em TIMESTAMP DEFAULT NOW(),

    CONSTRAINT transacoes_pk PRIMARY KEY (id),
    CONSTRAINT transacoes_fk FOREIGN KEY (cliente_id) REFERENCES banco.clientes(id)
);

DO $$
BEGIN
  INSERT INTO banco.clientes (nome, limite)
  VALUES
    ('Jovane', 1000 * 100),
    ('Natalie', 800 * 100),
    ('Diana', 10000 * 100),
    ('Camile', 100000 * 100),
    ('Next Child', 5000 * 100);
END; $$
