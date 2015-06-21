var items;

    function onlyUnique(value, index, self) { 
        return self.indexOf(value) === index;
    }
    
    function getData(d)
    {
        console.log("inside get data");
        items = Object.keys(d).map(function(key) {

            return [key, d[key]]; 
        });
        console.log(items[1][1]);
        var hindiMovies=[];
        var allLanguages=[];
        for (var i=0;i<items.length;i++){
            for(var j=0;j<items[i][1][4].length;j++)
            {
                console.log(items[i][1][4][j]);
                allLanguages.push(items[i][1][4][j]);    
            
            
                if(items[i][1][4][j]=="Hindi" || items[i][1][4][j]=="")
                {
                    hindiMovies.push(items[i]);
                }
            }
        }
        allLanguages.push("All");

        var uniqueLanguages = allLanguages.filter( onlyUnique );

        addLanguages(uniqueLanguages);

        // Sort the array based on the second element
        hindiMovies.sort(function(first, second) {
            return second[1][1] - first[1][1]; });
        
        addVideos(hindiMovies);

    }
    function addLanguages(uniqueLanguages){
        var sel=$('#uniqueLang');
        sel.text('');

        for(var i = 0; i < uniqueLanguages.length; i++) {
            var opt = $('<option>');
            opt.text(uniqueLanguages[i]);
            opt.value = uniqueLanguages[i];
            if(uniqueLanguages[i]=="Hindi")
                opt.attr("selected","selected");
            sel.append(opt);
        }
    }
    $(function(){
        $('#uniqueLang').on('change',function(){

            var filteMovies=[];
            var selectedLang=this.value;

            if (selectedLang=="All")
            {
            	for (var i=0 ; i<items.length;i++){
            		filteMovies.push(items[i]);
            	}
            }
            else {


            for (var i=0;i<items.length;i++){
                for(var j=0;j<items[i][1][4].length;j++){
                    if(items[i][1][4][j]==selectedLang){
                        filteMovies.push(items[i]);
                    }
            }

        }

    }
        $('#moviesdiv').text('');
        filteMovies.sort(function(first, second) {
            return second[1][1] - first[1][1]; });

        addVideos(filteMovies);


        });

    });