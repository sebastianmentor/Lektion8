from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate, upgrade
from views.forms import KontaktaOssForm
from models import db, seed_data, Bok, Kund, Bestallning, BestallningsDetalj

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost/LLB'
app.secret_key = 'askdfjöaslkjfölkjewöqpijf '


db.app = app
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def index():
    return render_template("index.html", active_page = 'start_page')

@app.route('/bocker')
def bocker():
    sort_column = request.args.get('sort_column', 'titel')
    sort_order = request.args.get('sort_order', 'asc')
    page = request.args.get('page', 1, type=int)
    

    all_books = Bok.query.all()

    return render_template(
        "bocker.html", 
        all_books=all_books, 
        active_page = 'bocker_page', 
        sort_column=sort_column,
        sort_order=sort_order,
        page=page)

@app.route('/bocker/bok/<bokid>')
def bok(bokid):
    # b = Bok.query.filter_by(id=bokid).first()
    # b = Bok.query.where(Bok.id == bokid).first()
    b = Bok.query.filter(Bok.id == bokid).first()
    return render_template("bok.html", bok=b, active_page = 'bocker_page')

@app.route('/kontakt', methods = ['GET', 'POST'])
def kontakt():
    form = KontaktaOssForm(request.form)

    if form.validate_on_submit():
        print(form.name.data)
        print(type(form.name))
        print(form.email.data)
        print(form.text.data)
        print(form.data)
        return redirect(url_for('index'))
        

    return render_template("kontakt.html", active_page = 'kontakt_page', form=form)

@app.route('/kunder')
def kunder():
    sort_column = request.args.get('sort_column', 'namn')
    sort_order = request.args.get('sort_order', 'asc')
    page=request.args.get('page', 1, type=int)
    search_word = request.args.get('q', '')

    sökta_kunder = Kund.query.filter(
        Kund.namn.like("%" + search_word+ "%") |
        Kund.adress.like("%" + search_word+ "%") |
        Kund.epost.like("%" + search_word+ "%") |
        Kund.telefonnummer.like("%" + search_word+ "%") 
    )

    if sort_column == 'namn':
        search_by = Kund.namn
    elif sort_column == 'epost':
        search_by = Kund.epost
    elif sort_column == 'telefonnummer':
        search_by = Kund.telefonnummer
    elif sort_column == 'adress':
        search_by = Kund.adress
    else:
        raise ValueError('Ingen match på acs')
    
    search_by = search_by.asc() if sort_order == 'asc' else search_by.desc()

    alla_kunder = sökta_kunder.order_by(search_by)
        
    pa_obj = alla_kunder.paginate(page=page, per_page=20,error_out=True)

    return render_template(
        "kunder.html", 
        kunderna=pa_obj.items, 
        active_page = 'kund_page',
        page=page ,
        pages = pa_obj.pages,
        has_next=pa_obj.has_next,
        has_prev=pa_obj.has_prev,
        sort_column=sort_column,
        sort_order=sort_order,
        q=search_word
        )


@app.route('/kund/<kundid>')
def kund(kundid):
    våran_kund = Kund.query.filter_by(id=kundid).first()
    # kundens_beställningar = Bestallning.query.filter_by(kund_id=kundid).all()
    
    return render_template("kund.html", kund=våran_kund, active_page = 'kund_page')

@app.route('/orders/<bestallningid>')
def orders(bestallningid):
    bestallt = Bestallning.query.filter_by(id=bestallningid).first()

    return render_template("bestallningsdetaljer.html", bestallning=bestallt, active_page = 'kund_page' )


if __name__ == '__main__':
    with app.app_context():
        upgrade()
        seed_data()

    app.run(debug=True)