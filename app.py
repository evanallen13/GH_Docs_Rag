from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    user_input = ''
    output_text = ''

    if request.method == 'POST':
        user_input = request.form.get('input_text', '')
        # Example processing: convert input to uppercase
        output_text = user_input.upper()

    return render_template('form.html', input_text=user_input, output_text=output_text)

if __name__ == '__main__':
    app.run(debug=True)
