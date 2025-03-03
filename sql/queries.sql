SELECT count(*) FROM `sicooperative`.`associado`; -- 100

SELECT * FROM `sicooperative`.`associado` order by 1;

--

SELECT count(*) FROM `sicooperative`.`conta`; -- 150

SELECT * FROM `sicooperative`.`conta`;

--

SELECT count(*) FROM `sicooperative`.`cartao`;

SELECT * FROM `sicooperative`.`cartao`;

-

SELECT count(*) FROM `sicooperative`.`movimento`;

SELECT * FROM `sicooperative`.`movimento`;

--

SELECT * FROM `sicooperative`.`associado` where id_associado = 1;

SELECT * FROM `sicooperative`.`conta` where id_associado = 1;

SELECT * FROM `sicooperative`.`cartao` where id_conta in (86,85);

--

select count(*) from sicooperative.associado where id_associado not in (select id_associado from sicooperative.conta);

select count(*) from sicooperative.conta where id_conta not in (select id_conta from sicooperative.cartao);

--

UPDATE sicooperative.cartao ca
JOIN sicooperative.conta co ON ca.id_conta = co.id_conta
JOIN sicooperative.associado a ON a.id_associado = co.id_associado
SET ca.nome_impresso_cartao = UPPER(CONCAT(a.nome_associado, ' ', a.sobrenome_associado));
