/* trocar modo de tela */
const iconeDark = document.getElementById("modo-dark");

if (iconeDark) {
    iconeDark.addEventListener("click", function () {
        document.body.classList.toggle("dark");
    });
}

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
        { value: "similar", texto: "Nome similar" },
        { value: "nome", texto: "Nome exato" },
        { value: "cargo", texto: "Cargo" },
        { value: "uf", texto: "UF"},
        { value: "orgao", texto: "Órgão" },
        { value: "buscacombinada", texto: "Busca Combinada"}
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

/* quantidade de registros exibidos por página */
const REGISTROS_POR_PAGINA = 10;

/* guarda os resultados e a página atual de cada tabela */
const resultados = {
    carreira: [],
    aposentados: []
};

const paginasAtuais = {
    carreira: 1,
    aposentados: 1
};

/* oculta as tabelas - aparecendo só depois de fazer uma consulta */
function ocultarTabelas() {
    if (tabCarreira) {
        tabCarreira.hidden = true;
    }

    if (tabAposentados) {
        tabAposentados.hidden = true;
    }
}

ocultarTabelas();

/* obtém ou cria a área de paginação de cada tabela */
function obterPaginacao(idTabela) {
    const tabela = document.getElementById(idTabela);

    if (!tabela) {
        return null;
    }

    const container = tabela.closest(".tabela") || tabela.parentElement;

    let paginacao = container.querySelector(
        `.paginacao[data-tabela="${idTabela}"]`
    );

    if (!paginacao) {
        paginacao = document.createElement("div");
        paginacao.className = "paginacao";
        paginacao.dataset.tabela = idTabela;
        paginacao.setAttribute(
            "aria-label",
            "Paginação dos resultados"
        );

        container.appendChild(paginacao);
    }

    return paginacao;
}

/* monta os botões de paginação */
function montarPaginacao(idTabela, totalRegistros) {
    const paginacao = obterPaginacao(idTabela);

    if (!paginacao) {
        return;
    }

    paginacao.replaceChildren();

    const chave = idTabela === "tabela-carreira"
        ? "carreira"
        : "aposentados";

    const totalPaginas = Math.ceil(
        totalRegistros / REGISTROS_POR_PAGINA
    );

    /* não mostra os controles quando existe apenas uma página */
    if (totalPaginas <= 1) {
        paginacao.hidden = true;
        return;
    }

    paginacao.hidden = false;

    const paginaAtual = paginasAtuais[chave];

    /* botão Anterior */
    const anterior = document.createElement("button");
    anterior.type = "button";
    anterior.textContent = "Anterior";
    anterior.className = "pagina-btn";
    anterior.disabled = paginaAtual === 1;

    anterior.addEventListener("click", function () {
        if (paginasAtuais[chave] > 1) {
            paginasAtuais[chave]--;
            atualizarTabela(idTabela);
        }
    });

    paginacao.appendChild(anterior);

    /* mostra a primeira página, a última e as páginas próximas da atual */
    const paginasVisiveis = new Set([
        1,
        totalPaginas,
        paginaAtual - 1,
        paginaAtual,
        paginaAtual + 1
    ]);

    const numeros = [...paginasVisiveis]
        .filter(function (numero) {
            return numero >= 1 && numero <= totalPaginas;
        })
        .sort(function (a, b) {
            return a - b;
        });

    let ultimaPagina = 0;

    numeros.forEach(function (numero) {
        /* mostra reticências quando existem páginas omitidas */
        if (ultimaPagina !== 0 && numero - ultimaPagina > 1) {
            const reticencias = document.createElement("span");
            reticencias.textContent = "…";
            reticencias.className = "pagina-reticencias";
            paginacao.appendChild(reticencias);
        }

        const botao = document.createElement("button");
        botao.type = "button";
        botao.textContent = String(numero);
        botao.className = "pagina-btn";

        if (numero === paginaAtual) {
            botao.classList.add("ativa");
            botao.setAttribute("aria-current", "page");
        }

        botao.addEventListener("click", function () {
            paginasAtuais[chave] = numero;
            atualizarTabela(idTabela);
        });

        paginacao.appendChild(botao);
        ultimaPagina = numero;
    });

    /* botão Próxima */
    const proxima = document.createElement("button");
    proxima.type = "button";
    proxima.textContent = "Próxima";
    proxima.className = "pagina-btn";
    proxima.disabled = paginaAtual === totalPaginas;

    proxima.addEventListener("click", function () {
        if (paginasAtuais[chave] < totalPaginas) {
            paginasAtuais[chave]++;
            atualizarTabela(idTabela);
        }
    });

    paginacao.appendChild(proxima);
}

/* monta a tabela com os registros da página atual */
function atualizarTabela(idTabela) {
    const tabela = document.getElementById(idTabela);

    if (!tabela) {
        return;
    }

    const chave = idTabela === "tabela-carreira"
        ? "carreira"
        : "aposentados";

    const registros = resultados[chave];

    const cabecalho = tabela.querySelector("thead");
    const corpo = tabela.querySelector("tbody");

    cabecalho.replaceChildren();
    corpo.replaceChildren();

    /* quando não há resultados */
    if (registros.length === 0) {
        const linha = document.createElement("tr");
        const celula = document.createElement("td");

        celula.colSpan = idTabela === "tabela-carreira" ? 8 : 18;
        celula.textContent = "Nenhum registro encontrado.";

        linha.appendChild(celula);
        corpo.appendChild(linha);

        montarPaginacao(idTabela, 0);
        atualizarContador(chave, 0, 0, 0);

        return;
    }

    /* monta o cabeçalho com as colunas vindas do DB */
    const colunas = Object.keys(registros[0]);
    const linhaCabecalho = document.createElement("tr");

    colunas.forEach(function (coluna) {
        const th = document.createElement("th");
        th.textContent = coluna.replaceAll("_", " ");
        linhaCabecalho.appendChild(th);
    });

    cabecalho.appendChild(linhaCabecalho);

    /* calcula quais registros pertencem à página atual */
    const paginaAtual = paginasAtuais[chave];
    const inicio = (paginaAtual - 1) * REGISTROS_POR_PAGINA;
    const fim = inicio + REGISTROS_POR_PAGINA;

    const registrosPagina = registros.slice(inicio, fim);

    /* vai preenchendo as linhas e colunas da página */
    registrosPagina.forEach(function (registro) {
        const linha = document.createElement("tr");

        colunas.forEach(function (coluna) {
            const celula = document.createElement("td");
            const valor = registro[coluna];

            if (valor === null || valor === undefined) {
                celula.textContent = "—";
            } else if (typeof valor === "object") {
                celula.textContent = JSON.stringify(valor);
            } else {
                /* remove espaços extras presentes em alguns campos do CSV */
                celula.textContent = String(valor).trim() || "—";
            }

            linha.appendChild(celula);
        });

        corpo.appendChild(linha);
    });

    /* atualiza os controles e o contador da tabela */
    montarPaginacao(idTabela, registros.length);

    const primeiro = inicio + 1;
    const ultimo = Math.min(fim, registros.length);

    atualizarContador(
        chave,
        primeiro,
        ultimo,
        registros.length
    );
}

/* atualiza a mensagem com o intervalo de registros exibido */
function atualizarContador(chave, primeiro, ultimo, total) {
    const contador = document.getElementById(`contador-${chave}`);

    if (!contador) {
        return;
    }

    if (total === 0) {
        contador.textContent = "Nenhum registro encontrado.";
    } else {
        contador.textContent =
            `Exibindo ${primeiro}–${ultimo} de ${total} registros`; 
    }
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
            statusConsulta.textContent =
                "Digite algo para realizar a consulta.";
        }
        return;
    }

    consultaEmAndamento = true;

    if (statusConsulta) {
        statusConsulta.textContent = "Consultando o DB...";
    }

    try {
        /* manda a requisição para o app.py */
        const url = new URL("/api/servidores", window.location.origin);

        /* define o parâmetro de acordo com o tipo de busca */
        const modoBusca = tipoBusca ? tipoBusca.value : "similar";

        if (modoBusca === "similar") {
            /* busca por similaridade de nome */
            const padrao = "%" + consulta.split(/\s+/).join("%") + "%";
            url.searchParams.set("similar", padrao);

            /* limita a busca por nome similar em até 100 resultados por tabela */
            url.searchParams.set("limit", "100");

        } else if (modoBusca === "nome") {
            /* realiza busca pelo nome exato */
            url.searchParams.set("nome", consulta.toUpperCase());

        } else if (modoBusca === "cargo") {
            /* realiza busca pelo cargo / emprego */
            url.searchParams.set("cargo", consulta.toUpperCase());

        } else if (modoBusca === "uf") {
            /* realiza busca por UF */ 
            url.searchParams.set("uf", consulta.toUpperCase());

        } else if (modoBusca === "orgao") {
            /* realiza busca por órgão / instituição */
            url.searchParams.set("orgao", consulta.toUpperCase());

        } else if (modoBusca === "buscacombinada") {
        /* segue a ordem nome exato, cargo, uf e órgão - usa ; entre os campos */
            
            /* nome similar ficou de fora para não ficar redundante já que tem o nome exato */
            const campos = consulta.split(";");

            if (campos.length > 4) {
                throw new Error(
                    "Informe no máximo quatro campos, separados por ponto e vírgula (;)."
                );
            }

            const nome = (campos[0] || "").trim();
            const cargo = (campos[1] || "").trim();
            const uf = (campos[2] || "").trim();
            const orgao = (campos[3] || "").trim();

            if (![nome, cargo, uf, orgao].some(Boolean)) {
                throw new Error("Informe pelo menos um critério de busca.");
            }

            if (nome) {
                url.searchParams.set("nome", nome.toUpperCase());
            }

            if (cargo) {
                url.searchParams.set("cargo", cargo.toUpperCase());
            }

            if (uf) {
                url.searchParams.set("uf", uf.toUpperCase());
            }

            if (orgao) {
                url.searchParams.set("orgao", orgao.toUpperCase());
            }
        }

        /* solicita os dados ao backend */
        const resposta = await fetch(url.toString(), {
            method: "GET",
            headers: { "Accept": "application/json" }
        });

        if (!resposta.ok) {
            throw new Error(`Erro HTTP: ${resposta.status}`);
        }

        const dados = await resposta.json();

        /* formato esperado da resposta */
        if (
            !dados ||
            !Array.isArray(dados.carreira) ||
            !Array.isArray(dados.aposentados)
        ) {
            throw new Error("Formato de resposta inválido.");
        }

        /* guarda os resultados completos recebidos da API */
        resultados.carreira = dados.carreira;
        resultados.aposentados = dados.aposentados;

        /* toda nova pesquisa começa na primeira página */
        paginasAtuais.carreira = 1;
        paginasAtuais.aposentados = 1;

        /* verifica em qual tabela foram encontrados resultados */
        const verificaCarreira = resultados.carreira.length > 0;
        const verificaAposentados = resultados.aposentados.length > 0;

        /* mostra ou oculta cada tabela de acordo com os resultados */
        if (tabCarreira) {
            tabCarreira.hidden = !verificaCarreira;
        }

        if (tabAposentados) {
            tabAposentados.hidden = !verificaAposentados;
        }

        /* monta a tabela Carreira, caso existam resultados */
        if (verificaCarreira) {
            atualizarTabela("tabela-carreira");
        }

        /* monta a tabela Aposentados, caso existam resultados */
        if (verificaAposentados) {
            atualizarTabela("tabela-aposentados");
        }

        /* mensagens de resultado da consulta */
        const totalCarreira = resultados.carreira.length;
        const totalAposentados = resultados.aposentados.length;

        if (verificaCarreira && verificaAposentados) {
            statusConsulta.textContent =
                `Foram encontrados ${totalCarreira} registros na tabela ` +
                `Carreira e ${totalAposentados} registros na tabela Aposentados.`;

        } else if (verificaCarreira) {
            statusConsulta.textContent =
                `Foram encontrados ${totalCarreira} registro(s) na tabela Carreira.`;

        } else if (verificaAposentados) {
            statusConsulta.textContent =
                `Foram encontrados ${totalAposentados} registro(s) na tabela Aposentados.`;

        } else {
            statusConsulta.textContent =
                "Nenhum registro foi encontrado para essa consulta.";
        }

    } catch (erro) {
        console.error("Erro ao realizar a consulta:", erro);

        /* limpa os resultados quando ocorre um erro */
        resultados.carreira = [];
        resultados.aposentados = [];

        paginasAtuais.carreira = 1;
        paginasAtuais.aposentados = 1;

        ocultarTabelas();

        /* esconde os controles de paginação existentes */
        ["tabela-carreira", "tabela-aposentados"].forEach(function (idTabela) {
            const paginacao = obterPaginacao(idTabela);

            if (paginacao) {
                paginacao.hidden = true;
                paginacao.replaceChildren();
            }
        });

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
