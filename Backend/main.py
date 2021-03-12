from ApiFolder import create_main


app = create_main()

if __name__ == '__main__':
    app.run(debug=True)