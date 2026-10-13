/* trocar modo de tela */ 
const iconeDark = document.getElementById("modo-dark");

iconeDark.addEventListener("click", function(){
    document.body.classList.toggle("dark");
});

const formulario = document.getElementById("pesquisar");

const campoConsulta = formulario
    ? formulario.querySelector('input[name="input"]')
    : null;

/* mostra na tela qual tipo de pesquisa/busca o usuário quer fazer */
let tipoBusca = null;

if (formulario && campoConsulta) {
    tipoBusca = document.createElement("select");
    tipoBusca.id = "tipo-busca";
    tipoBusca.setAttribute("aria-label", "Tipo de busca");

    const opcoesBusca = [
        { value: "similar", texto: "Nome similar" }, /* por enquanto busca por nome similar, nome exato, cargo/emprego e órgão/instituição */ 
        { value: "nome", texto: "Nome exato" },
        { value: "cargo", texto: "Cargo" },
        { value: "orgao", texto: "Órgão" }
    ];

    opcoesBusca.forEach(function (opcao) {
        const elemento = document.createElement("option");
        elemento.value = opcao.value;
        elemento.textContent = opcao.texto;
        tipoBusca.appendChild(elemento);
    });

    const barraPesquisa = document.getElementById("barra-pesquisar");

    if (barraPesquisa) {
        barraPesquisa.insertAdjacentElement("beforebegin", tipoBusca);
    }
}

const tipoConsulta = document.getElementById("tipo-consulta");
const statusConsulta = document.getElementById("status-consulta");
let consultaEmAndamento = false;

const tabCarreira = document
    .getElementById("tabela-carreira")
    ?.closest(".tabela");

const tabAposentados = document
    .getElementById("tabela-aposentados")
    ?.closest(".tabela");


function ocultarTabelas() {
    if (tabCarreira) {
        tabCarreira.hidden = true;
    }

    if (tabAposentados) {
        tabAposentados.hidden = true;
    }
}

ocultarTabelas(); /* oculta as tabelas - aparecendo só depois de fazer uma consulta*/

/* para montar as tabelas */ 
function montarTabela(idTabela, registros, quantidadeColunas, mensagem = "Nenhum registro encontrado.") {
    const tabela = document.getElementById(idTabela);

    if (!tabela) {
        return 0;
    }

    const cabecalho = tabela.querySelector("thead");
    const corpo = tabela.querySelector("tbody");

    cabecalho.replaceChildren();
    corpo.replaceChildren();

    if (!Array.isArray(registros) || registros.length === 0) {
        const linha = document.createElement("tr");
        const celula = document.createElement("td");

        celula.colSpan = quantidadeColunas;
        celula.textContent = mensagem;

        linha.appendChild(celula);
        corpo.appendChild(linha);

        return 0;
    }

    /* monta as linhas e colunas */
    const colunas = Object.keys(registros[0]);
    const linhaCabecalho = document.createElement("tr");

    colunas.forEach(function (coluna) {
        const th = document.createElement("th");
        th.textContent = coluna.replaceAll("_", " ");
        linhaCabecalho.appendChild(th);
    });

    cabecalho.appendChild(linhaCabecalho);

    /* vai preenchendo as linhas da tabela */
    registros.forEach(function (registro) {
        const linha = document.createElement("tr");

        colunas.forEach(function (coluna) {
            const celula = document.createElement("td");
            const valor = registro[coluna];

            if (valor === null || valor === undefined) {
                celula.textContent = "—";
            } else if (typeof valor === "object") {
                celula.textContent = JSON.stringify(valor);
            } else {
                celula.textContent = String(valor);
            }

            linha.appendChild(celula);
        });

        corpo.appendChild(linha);
    });

    return registros.length;
}

/* faz a consulta ao DB */ 
async function realizarConsulta() {
    if (!campoConsulta || consultaEmAndamento) {
        return;
    }

    const consulta = campoConsulta.value.trim();

    /* caso o usuário clique em ENTER sem ter digitado nada */ 
    if (!consulta) {
        if (statusConsulta) {
            statusConsulta.textContent = "Digite algo para realizar a consulta.";
        }
        return;
    }

    consultaEmAndamento = true;

    if (statusConsulta) {
        statusConsulta.textContent = "Consultando o DB";
    }

    try {
        /* manda a resposta pro app.py */ 
        const url = new URL("/api/servidores", window.location.origin);

        /* define o parâmetro de acordo com o tipo de busca */
        const modoBusca = tipoBusca ? tipoBusca.value : "similar";

        if (modoBusca === "similar") {
            /* busca por similaridade de nome */ 
            const padrao = "%" + consulta.split(/\s+/).join("%") + "%";
            url.searchParams.set("similar", padrao);
            url.searchParams.set("limit", "100"); /* limita a busca por nome similar em até 100 resultados para as duas tabelas */ 

        } else if (modoBusca === "nome") {
            /* realiza busca pelo nome exato */
            url.searchParams.set("nome", consulta.toUpperCase());

        } else if (modoBusca === "cargo") {
            /* realiza busca pelo cargo / emprego */
            url.searchParams.set("cargo", consulta.toUpperCase());

        } else if (modoBusca === "orgao") {
            /* realiza busca por órgão / instituição */
            url.searchParams.set("orgao", consulta.toUpperCase()); /* converte todas as consultas para maiúsculo - formato que tá no DB */ 
        }
      
        /* solicita os dados ao backend */ 
        const resposta = await fetch(url.toString(), {
            method: "GET",
            headers: {"Accept": "application/json"}
        });

        if (!resposta.ok) {
            throw new Error(`Erro HTTP: ${resposta.status}`);
        }

        const dados = await resposta.json();

        /* formato da resposta */
        if (!dados || !Array.isArray(dados.carreira) || !Array.isArray(dados.aposentados)) {
            throw new Error("Formato de resposta inválido.");
        }

        /* verifica em qual tabela foi (foram) encontrado(s) resultados da consulta */ 
        const verificaCarreira = dados.carreira.length > 0;
        const verificaAposentados = dados.aposentados.length > 0;

        ocultarTabelas();

        /* caso de ter registros apenas na tabela carreira*/ 
        if (verificaCarreira && !verificaAposentados) {

            /* se encontrar resultados monta a tabela carreira com a quantidade de colunas vinda do DB */
            if (tabCarreira) {
                tabCarreira.hidden = false;
            }

            const totalRegistros = montarTabela("tabela-carreira", dados.carreira, 8);
            statusConsulta.textContent = `Foram encontrado(s) ${totalRegistros} registro(s) na tabela Carreira.`;

    /* caso de ter apenas registros na tabela de aposentados */ 
    } else if (verificaAposentados && !verificaCarreira) {

        /* se encontrar resultados monta a tabela Aposentados já pegando a quantidade de colunas do DB */ 
        if (tabAposentados) {
            tabAposentados.hidden = false;
        }

        /* 18 colunas */
        const totalRegistros = montarTabela( "tabela-aposentados", dados.aposentados, 18);

        statusConsulta.textContent = `Foram encontrado(s) ${totalRegistros} registro(s) na tabela Aposentados.`;

    /* caso de ter registros em ambas as tabelas*/ 
    } else if (verificaCarreira && verificaAposentados) {

        /* se encontrar resultados em ambas as tabelas mostra essa mensagem na tela */
        statusConsulta.textContent = "Foram encontrados resultados em ambas as tabelas. Realize uma nova consulta.";

    /* quando não tem registro em nenhuma tabela */ 
    } else {

       /* senão encontrar nenhum registro mostra essa mensagem na tela */ 
        statusConsulta.textContent = "Nenhum registro foi encontrado para essa consulta.";
    }

    } catch (erro) {
        console.error("Erro ao realizar a consulta:", erro);

        /* se der erro não monta a tabela */ 
        montarTabela("tabela-carreira", [], 8, "Não foi possível carregar os registros.");

        montarTabela("tabela-aposentados", [], 18, "Não foi possível carregar os registros.");

        if (statusConsulta) {
            statusConsulta.textContent =
                "Não foi possível realizar a consulta. Verifique o servidor e tente novamente.";
        }

    } finally {
        consultaEmAndamento = false;
    }
}

/* usuário envia a consulta clicando em ENTER */ 
if (campoConsulta && formulario) {

    campoConsulta.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            realizarConsulta();
        }
    });

    formulario.addEventListener("submit", function (event) {
        event.preventDefault();
        realizarConsulta();
    });
}
