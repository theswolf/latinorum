var loki = require('lokijs');

var db = new loki("./test.db");

var fs = require('fs');

var collection = [];

fs.readFile('./versioni.json', 'utf8', function(err, data) {
    if (err) throw err; // we'll not consider error handling for now
    var obj = JSON.parse(data);
    var dataTypes = []
    obj.map(function(data) {
        var type = data['data-type'];
        if (dataTypes.indexOf(type) == -1) {
            dataTypes.push(type);
            switch (type) {
                case 'autore':
                    collection['autore'] = db.addCollection('autori', {
                        indices: ['autore']
                    });
                    break;
                case 'versione':
                    collection['versione'] = db.addCollection('versioni', {
                        indices: ['autore']
                    });
                    break;
                case 'dettaglio':
                    collection['dettaglio'] = db.addCollection('dettagli', {
                        indices: ['autore', 'titolo', 'capitolo']
                    });
                    break;

                case 'traduzione':
                    collection['traduzione'] = db.addCollection('traduzione', {
                        indices: ['originale', 'traduzione', 'capitolo']
                    });
            }

        }



    });

    obj.map(function(data) {
        collection[data['data-type']].insert(data);
    });
    //console.log(data['data-type']);

    db.saveDatabase();
});