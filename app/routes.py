# Rotas e Manipuladores de visualização
from flask import Blueprint, render_template, session, request, url_for, redirect, Response, make_response, jsonify
from app.models import db, Venda, Corretor, Imovel, Cliente, Condicao, Tipo
import locale
import re
from app.util import clean_currency_string
from sqlalchemy import func
from functools import reduce

bp = Blueprint('routes', __name__)

# FILTERS
@bp.app_template_filter()
def filterCurrency(valor):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    valor = locale.currency(valor, grouping=True, symbol=None)
    return 'R$ %s' % valor

@bp.app_template_filter()
def filterPhone(value):
	telFormatado = '({}) {}-{}-{}'.format(value[0:2], value[2] ,value[3:7], value[7:])
	return telFormatado

@bp.app_template_filter()
def filterCpf(value):
	telFormatado = '{}.{}.{}-{}'.format(value[0:3], value[3:6] ,value[6:9], value[9:])
	return telFormatado

@bp.app_template_filter()
def filterDate(date):
	formatedDate = date.strftime("%d/%m/%Y")
	return formatedDate

@bp.app_template_filter()
def filterCep(cep):
	formatedCep = '{}-{}'.format(cep[0:5], cep[5:])
	return formatedCep
# ROUTES

@bp.route('/')
def index():
	if 'user' in session:
		return redirect(url_for('routes.panel'), user = session['user'])
		# return render_template('panel.html', user = session['user'])
	return render_template('login.html')

@bp.route('/panel')
def panel():
	if 'user' in session:
		imoveis = db.session.query(Imovel).outerjoin(Venda).filter(Venda.id_corretor == None)
		totalImoveis = imoveis.count()
		vendas = db.session.query(Venda).filter(Venda.id_corretor == session['user']['id'])
		totalVendas = vendas.count()
		totalClientes = db.session.query(Cliente).count()
		comissao = 0
		for venda in vendas:
			comissao += venda.valor_comissao
			
		return render_template('panel.html', user = session['user'], imoveis = imoveis, 
			 totalImoveis = totalImoveis, vendas=totalVendas, 
			 totalClientes=totalClientes, comissao = comissao)
	
	return render_template('login.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		
		corretor = Corretor.query.filter_by(nome=username, senha=password).first()

		if corretor is not None:
			session['user'] = {"id": corretor.id, "nome": corretor.nome}
			return redirect(url_for('routes.panel'))
		else:
			return render_template('login.html', flag = False)
		
	return render_template('login.html')

@bp.route('/logout')
def logout():
	session.pop('user', '')
	return redirect('/')

## ROTAS DE IMOVEIS

@bp.route('/imovel/delete/<int:id>')
def deleteImovel(id):
	imovel = db.get_or_404(Imovel, id)
	db.session.delete(imovel)
	db.session.commit()
	return redirect(url_for('routes.panel'))

@bp.route('/imovel/edit/<int:id>', methods=['GET', 'POST'])
def editImovel(id):
	imovel = db.get_or_404(Imovel, id)

	if request.method == 'POST':
		imovel.nome = request.form['nome'].lower()
		imovel.tipo_id = re.sub(r'[^0-9]', '', request.form['tipo'])
		imovel.cep = re.sub(r'[^0-9]', '', request.form['cep'])
		imovel.logradouro = request.form['logradouro'].lower()
		imovel.bairro = request.form['bairro'].lower()
		imovel.cidade = request.form['cidade'].lower()
		imovel.numero = re.sub(r'[^0-9]', '', request.form['numero'])
		imovel.complemento = request.form['complemento'].lower()
		imovel.valor = clean_currency_string(request.form['valor'])

		db.session.commit()

		return redirect(url_for('routes.panel'))
	
	tipos = db.session.query(Tipo).all()
	return render_template('editImovel.html', imovel = imovel, user = session['user'], tipos = tipos)

## ROTA DE VENDAS
@bp.route('/vendidos')
def vendidos():
	imoveisVendidos = db.session.query(Imovel).join(Venda).filter(Venda.id_corretor == session['user']['id'])

	return render_template('vendidos.html', user = session['user'], imoveisVendidos = imoveisVendidos)

## ROTAS DE CLIENTES

@bp.route('/clientes')
def clientes():
	if 'user' in session:
		clientes = Cliente.query.all()
		return render_template('clientes.html', clientes = clientes, user = session['user'])
	return render_template('login.html')

@bp.route('/cliente/add', methods=['GET', 'POST'])
def clientesAdd():
	if request.method == 'POST':
		nome = request.form['nome'].lower()
		cpf = re.sub(r'[^0-9]', '', request.form['cpf'])
		email = request.form['email'].lower()
		telefone = re.sub(r'[^0-9]', '', request.form['telefone'])

		cliente = Cliente(nome, cpf, email, telefone)

		db.session.add(cliente)
		db.session.commit()

		return redirect(url_for('routes.clientes'))
	return render_template('addCliente.html', user = session['user'])


@bp.route('/cliente/delete/<int:id>')
def clientesDelete(id):
	cliente = db.get_or_404(Cliente, id)

	db.session.delete(cliente)
	db.session.commit()

	return redirect(url_for('routes.clientes'))

@bp.route('/cliente/update/<int:id>', methods=["GET", "POST"])
def clientesUpdate(id):
	cliente = db.get_or_404(Cliente, id)

	if request.method == 'POST':
		cliente.nome = request.form['nome'].lower()
		cliente.cpf = re.sub(r'[^0-9]', '', request.form['cpf'])
		cliente.email = request.form['email'].lower()
		cliente.telefone = re.sub(r'[^0-9]', '', request.form['telefone'])

		db.session.commit()

		return redirect(url_for('routes.clientes'))
	return render_template('editCliente.html', cliente = cliente, user = session['user'])

# ROTAS PARA MODAL DE SIMULAÇÃO 
@bp.route('/simulacao', methods=["POST", "GET"])
def ajaxfile():
	if request.method == 'POST':
		id = request.form['imovel_id']
		imovel = db.get_or_404(Imovel, id)
		clientes = Cliente.query.all()
		condicoes = Condicao.query.all()
		corretor = session['user']
		valorComissao = imovel.comissao * imovel.valor / 100
		
	return jsonify({'htmlresponse': render_template('modalSimulacao.html', 
						 imovel=imovel, corretor = corretor, 
						 clientes = clientes, 
						 condicoes = condicoes)})


@bp.route('/vender', methods=["POST", "GET"])
def test():
	if request.method == 'POST':
		id_cliente = request.form['id_cliente']
		id_condicao = request.form['id_condicao']
		id_corretor = request.form['id_corretor']
		id_imovel = request.form['id_imovel']
		valor_comissao = request.form['valor_comissao']

		venda = Venda(id_corretor, id_imovel, id_cliente, id_condicao, valor_comissao)
		db.session.add(venda)
		db.session.commit()
	return jsonify({'response': 'success'})


@bp.route('/extrato/<int:id>', methods=['POST', 'GET'])
def extrato(id):
	result = db.session.query(Venda, Imovel, Corretor, Cliente).join(Imovel, Venda.id_imovel==Imovel.id) \
	.join(Corretor, Venda.id_corretor == Corretor.id).join(Cliente, Venda.id_cliente == Cliente.id).first()

	if result:
		venda = result.Venda
		venda.condicao.nome
		imovel = result.Imovel
		imovel.tipo.nome
		corretor = result.Corretor
		cliente = result.Cliente
		
		return render_template('extrato.html', imovel = imovel, venda = venda, corretor = corretor, cliente = cliente)
	return {}



# Quem foi o vendedor, qual foi o imóvel, para quem foi vendido o imóvel e as condições de pagamento e extrato