const API_URL = "http://127.0.0.1:8000";

document.addEventListener("DOMContentLoaded", () => {
    if (window.location.pathname.includes("dashboard.html")) {
        verificarAutenticacao();
        carregarDadosIniciais();
    }
});


function verificarAutenticacao() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = 'index.html';
    }
}


function alternarTelas(tela) {
    const loginBox = document.getElementById('login-box');
    const cadastroBox = document.getElementById('cadastro-box');

    if (tela === 'cadastro') {
        loginBox.style.display = 'none';
        cadastroBox.style.display = 'block';
    } else {
        cadastroBox.style.display = 'none';
        loginBox.style.display = 'block';
    }
}


async function executarLogin() {
    const emailInput = document.getElementById('email').value;
    const senhaInput = document.getElementById('password').value;
    const btnEntrar = document.getElementById('btn-entrar');

    if (!emailInput || !senhaInput) {
        alert("Por favor, preencha todos os campos.");
        return;
    }

    btnEntrar.innerText = "Autenticando...";
    btnEntrar.disabled = true;

    const dadosLogin = {
        email: emailInput,
        password: senhaInput
    };

    try {
        const resposta = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dadosLogin)
        });

        if (resposta.ok) {
    const dados = await resposta.json();
    localStorage.setItem('access_token', dados.access_token);
    if (dados.username) {
        localStorage.setItem('user_name', dados.username);
    } else {
        localStorage.setItem('user_name', emailInput.split('@')[0]);
    }

    window.location.href = 'dashboard.html';
}

    } catch (erro) {
        console.error("Erro no login:", erro);
        alert(`Ocorreu um erro no código!\n\nMensagem: ${erro.message}`);
    } finally {
        btnEntrar.innerText = "Entrar na Conta";
        btnEntrar.disabled = false;
    }
}


async function executarCadastro() {
    const nameInput = document.getElementById('reg-name').value;
    const usernameInput = document.getElementById('reg-username').value;
    const emailInput = document.getElementById('reg-email').value;
    const senhaInput = document.getElementById('reg-password').value;
    const btnCadastrar = document.getElementById('btn-cadastrar');

    if (!nameInput || !usernameInput || !emailInput || !senhaInput) {
        alert("Por favor, preencha todos os campos para se cadastrar.");
        return;
    }

    btnCadastrar.innerText = "Cadastrando...";
    btnCadastrar.disabled = true;

    const dadosCadastro = {
        name: nameInput,
        username: usernameInput,
        email: emailInput,
        password: senhaInput
    };

    try {
        const resposta = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dadosCadastro)
        });

        if (resposta.ok) {
            alert("Conta criada com sucesso! Você já pode realizar o login.");

            document.getElementById('reg-name').value = '';
            document.getElementById('reg-username').value = '';
            document.getElementById('reg-email').value = '';
            document.getElementById('reg-password').value = '';
            alternarTelas('login');
        } else {
            const erroCorpo = await resposta.json();

            let mensagemErro = "Erro ao realizar cadastro.";
            if (typeof erroCorpo.detail === 'string') {
                mensagemErro = erroCorpo.detail;
            } else if (Array.isArray(erroCorpo.detail)) {
                mensagemErro = erroCorpo.detail.map(e => `${e.loc[1] || 'Campo'}: ${e.msg}`).join('\n');
            }

            alert(`Erro ao cadastrar:\n\n${mensagemErro}`);
        }
    } catch (erro) {
        console.error("Erro na requisição de cadastro:", erro);
        alert("Não foi possível conectar ao servidor para realizar o cadastro.");
    } finally {
        btnCadastrar.innerText = "Cadastrar";
        btnCadastrar.disabled = false;
    }
}


function renderizarExtrato(transacoes) {
    const tabela = document.getElementById('tabela-extrato');
    if (!tabela) return;

    tabela.innerHTML = "";

    if (!Array.isArray(transacoes) || transacoes.length === 0) {
        tabela.innerHTML = `<tr><td colspan="3" style="text-align:center; color:#888;">Nenhuma transação encontrada.</td></tr>`;
        return;
    }

    transacoes.forEach(t => {
        const linha = document.createElement('tr');
        const classeValor = t.tipo === 'deposito' ? 'valor-positivo' : 'valor-negativo';
        const sinal = t.tipo === 'deposito' ? '+' : '-';

        linha.innerHTML = `
            <td>${t.descricao || 'Operação'}</td>
            <td>${t.data ? new Date(t.data).toLocaleDateString('pt-BR') : '-'}</td>
            <td class="${classeValor}">${sinal} R$ ${(t.valor || 0).toFixed(2)}</td>
        `;
        tabela.appendChild(linha);
    });
}


async function carregarDadosIniciais() {
    const token = localStorage.getItem('access_token');

    try {
        const resConta = await fetch(`${API_URL}/me`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Accept': 'application/json'
            }
        });

        if (!resConta.ok) {
            console.error("Erro ao buscar conta:", await resConta.text());
            return;
        }

        const dadosConta = await resConta.json();

        const valorSaldo = dadosConta.balance !== undefined ? dadosConta.balance : 0;
        const elSaldo = document.getElementById('txt-saldo');
        if (elSaldo) {
            elSaldo.innerText = `R$ ${parseFloat(valorSaldo).toFixed(2)}`;
        }

        let nomeExibicao = dadosConta.titular || dadosConta.name || dadosConta.username || localStorage.getItem('user_name') || "Usuário";

        const elNome = document.getElementById('usuario-nome');
        if (elNome) {
            elNome.innerText = `Olá, ${nomeExibicao}`;
        }

        const avatarImg = document.getElementById('avatar-img');
        const fotoSalva = localStorage.getItem('user_avatar');

        if (fotoSalva && avatarImg) {
            avatarImg.src = fotoSalva;
        } else if (avatarImg) {
            avatarImg.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(nomeExibicao)}&background=0D6EFD&color=fff`;
        }

        const accountId = dadosConta.id;

        if (accountId) {
            const resHistorico = await fetch(`${API_URL}/history/${accountId}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (resHistorico.ok) {
                const transacoes = await resHistorico.json();
                renderizarExtrato(transacoes);
            } else {
                renderizarExtrato([]);
            }
        }

    } catch (erro) {
        console.error("Erro ao carregar dados do banco:", erro);
    }
}
    try {
    } catch (erro) {
        console.error("Erro ao carregar dados do banco:", erro);
    }

async function executarTransacao() {
    const token = localStorage.getItem('access_token');
    const tipo = document.getElementById('tipo-transacao').value;
    const destino = document.getElementById('destino').value;
    const valor = parseFloat(document.getElementById('valor').value);

    if (!valor || valor <= 0) {
        alert("Insira um valor válido.");
        return;
    }

    const payload = {
        tipo_operacao: tipo,
        conta_destino_id: destino,
        valor: valor
    };

    try {
        const response = await fetch(`${API_URL}/transaction/execute`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            alert("Operação realizada com sucesso!");
            carregarDadosIniciais();
        } else {
            const erroData = await response.json();
            alert(`Erro: ${erroData.detail || "Não foi possível concluir a operação."}`);
        }
    } catch (erro) {
        console.error("Erro ao processar transação:", erro);
    }
}


function toggleMenu() {
    const menu = document.getElementById('dropdown-menu');
    if (menu) {
        menu.classList.toggle('show');
    }
}

window.addEventListener('click', (e) => {
    if (!e.target.closest('.user-profile-container')) {
        const menu = document.getElementById('dropdown-menu');
        if (menu && menu.classList.contains('show')) {
            menu.classList.remove('show');
        }
    }
});

function alterarFoto(event) {
    const arquivo = event.target.files[0];
    if (arquivo) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const fotoBase64 = e.target.result;

            const avatarImg = document.getElementById('avatar-img');
            if (avatarImg) avatarImg.src = fotoBase64;

            localStorage.setItem('user_avatar', fotoBase64);
        };
        reader.readAsDataURL(arquivo);
    }
}

function abrirConfiguracoes() {
    alert("Painel de configurações em desenvolvimento.");
}

function fazerLogout() {
    if (confirm("Deseja realmente sair da sua conta?")) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_avatar');
        window.location.href = 'index.html';
    }
}