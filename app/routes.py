# Rotas e Manipuladores de visualização
from flask import Blueprint, render_template, session, request, url_for, redirect, jsonify
from app.models import db, Venda, Corretor, Imovel, Cliente, Condicao, Tipo
import re
from app.util import clean_currency_string

bp = Blueprint('routes', __name__)

############################################################# DEFINIÇÃO DE ROTAS
@bp.route('/')
def index():
	if 'user' in session:
		return redirect(url_for('routes.panel'), user = session['user'])
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

############################################################### ROTAS DASHBOARD

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





############################################################### ROTAS DE IMOVEIS

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
	imoveisVendidos = db.session.query(Imovel, Venda).join(Venda).filter(Venda.id_corretor == session['user']['id'])

	return render_template('vendidos.html', user = session['user'], imoveisVendidos = imoveisVendidos)

@bp.route('/venda/delete/<int:id>')
def deleteVenda(id):
	venda = db.get_or_404(Venda, id)
	db.session.delete(venda)
	db.session.commit()
	return redirect(url_for('routes.panel'))

############################################################### ROTAS DE CLIENTES

@bp.route('/clientes')
def clientes():
	flag = False if 'flag' in request.args else True

	if 'user' in session:
		clientes = Cliente.query.all()
		return render_template('clientes.html', clientes = clientes, user = session['user'], flag = flag)
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
	venda = Venda.query.filter_by(id_cliente=id).first()
	if venda:
		return redirect(url_for('routes.clientes', flag = False))
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



############################################################### ROTAS PARA VENDAS 
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
	result = db.session.query(Venda, Imovel, Corretor, Cliente).join(Imovel, Venda.id_imovel==id) \
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
