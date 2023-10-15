import xmlschema

def main():
    schema = "https://www.crossref.org/schemas/crossref5.3.0.xsd"
    xsd = xmlschema.XMLSchema(schema)
    f = "/Users/eshadatta/static-page-id-generator/submit_files/try_me.xml"
    try:
        xsd.validate(f)
    except Exception as e:
        print ("ERROR: ", e)
        exit(1)

if __name__ == "__main__":
    main()
