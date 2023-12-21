async function submitRequest(drawingData){
    const apiQueryString = `http://127.0.0.1:5000/api/mapping?coords=${drawingData.points}&start-date=${drawingData.startDate}&end-date=${drawingData.endDate}&imagery-type=${drawingData.imageMode}&aggregation-length=${drawingData.aggLenth}&aggregation-type=${drawingData.aggType}`;
    console.log(apiQueryString)
    /// Make query
    var response = await fetch(apiQueryString);

    if (response.ok) {


    var data = await response.json();}





}