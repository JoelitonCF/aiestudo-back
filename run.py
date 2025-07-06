from flask_backend import create_app


app = create_app()

if __name__ == "__main__":
    # O debug será controlado via FLASK_ENV=development ou
    # config.DEBUG no objeto de configuração
    app.run(host="0.0.0.0", port=int(app.config.get("PORT", 5000)))
