from flask import Flask, render_template, redirect, url_for

app = Flask( __name__ )

@app.route( '/home' )
def index():
    return render_template( 'layout.html' )

@app.route( '/yes', methods=['POST'] )
def yes_event():
    return redirect( url_for( 'index' ) )

@app.route( '/no', methods=['POST'] )
def no_event():
    return redirect( url_for( 'index' ) )


if __name__ == '__main__':
    app.run()
