        function addVideos(movlist)
        {
            $('#moviesdiv').text('');
            
            for(var i=0;i<movlist.length;i++)
            {
                var outerDiv=$("<div>").addClass("row");
                var innerVideoDiv=$("<div>").addClass("col-md-7");
                var videoAttrDiv=$("<div>").addClass("flex-video widescreen");
                var videoFrame=$("<iframe>").attr("height","220").attr("width","400").attr("src","http://www.youtube.com/embed/"+movlist[i][1][0]);
                var innerTxtDiv=$("<div>").addClass("col-md-5");
                
                var name = $("<h2>").text(movlist[i][0]).css("text-decoration","underline");

                var table = $("<table>").attr("width","80%");

                var rating;
                if(movlist[i][1][1]=='0')
                	rating =$("<tr>").append($("<td>").attr("width","40%").append($("<h4>").text("IMDB Rating:  ")),$("<td>").append($("<h4>").text("N/A")));
                else
                	rating = $("<tr>").append($("<td>").attr("width","40%").append($("<h4>").text("IMDB Rating:  ")),$("<td>").append($("<h4>").text(movlist[i][1][1])));
             
             	var duration;
             	if(movlist[i][1][2]=='')
					duration = $("<tr>").append($("<td>").attr("width","40%").append($("<h4>").text("Duration:  ")),$("<td>").append($("<h4>").text("N/A")));
				else
					duration = $("<tr>").append($("<td>").attr("width","40%").append($("<h4>").text("Duration:  ")),$("<td>").append($("<h4>").text(movlist[i][1][2])));

				var genre;
				if(movlist[i][1][3]=='')
                	genre = $("<tr>").append($("<td>").attr("width","40%").append($("<h4>").text("Genre:  ")),$("<td>").append($("<h4>").text("N/A")));
                else
                	genre = $("<tr>").append($("<td>").attr("width","40%").append($("<h4>").text("Genre:  ")),$("<td>").append($("<h4>").text(movlist[i][1][3])));

                var release_date;
				if(movlist[i][1][5]=='')
                	release_date = $("<tr>").append($("<td>").attr("width","40%").append($("<h4>").text("Release date:  ")),$("<td>").append($("<h4>").text("N/A")));
                else
                	release_date = $("<tr>").append($("<td>").attr("width","40%").append($("<h4>").text("Release date:  ")),$("<td>").append($("<h4>").text(movlist[i][1][5])));


                var videoAll = innerVideoDiv.append(videoAttrDiv.append(videoFrame));
                var textAll = innerTxtDiv.append(name,table.append(rating,duration,genre,release_date));

                $('#moviesdiv').append(outerDiv.append(videoAll,textAll),"<hr>");
            }


        }