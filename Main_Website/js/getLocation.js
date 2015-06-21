var DefaultCity="";
 var fillInPage = (function () {
    var updateCityText = function (geoipResponse) {
      console.log("caliing updateCityText ");
    DefaultCity=geoipResponse.city.names.en;
        console.log("city "+DefaultCity);
        console.log("longitude "+geoipResponse.location.longitude);
        console.log("latitude "+geoipResponse.location.latitude);
        return DefaultCity;
    };
 
    var onSuccess = function (geoipResponse) {
      console.log("caliing onSuccess of geoip2.city");
        return updateCityText(geoipResponse);
    };
 
    /* If we get an error we will */
    var onError = function (error) {
      console.log("Calling error of geoip2.city");
        return;
    };
 
    return function () {
      console.log("Calling geoip2.city");
        geoip2.city( onSuccess, onError );
    };
}());
 
 function getCityLocation(){
fillInPage();
//console.log(onSuccess);
return DefaultCity;
}