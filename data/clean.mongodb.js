use('products');

db.products.aggregate([
    {
        $match: {
            $expr: {
                $gt: [
                    { $size: { $objectToArray: "$specs" } },
                    0
                ]
            }
        }
    },
    {
        $out: "products_with_specs"
    }
]);

db.products_with_specs.find();
db.products_with_specs.find().size();

// docker exec nexatech - product mongoexport--db = products--collection = products_with_specs--out = /tmp/products_with_specs.json