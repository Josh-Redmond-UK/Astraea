async function submitRequest(drawingData){
    const apiQueryString = `http://localhost:5000/api/mapping?roi=${drawingData.points}&cloud_cover=100&start_date=${drawingData.startDate}&end_date=${drawingData.endDate}&image_type=${drawingData.imageMode}&aggregation_length=${drawingData.aggLenth}&aggregation_type=${drawingData.aggType}`;
    console.log(apiQueryString)
    /// Make query
    var response = await fetch(apiQueryString);

    if (response.ok) {


    var data = await response.json();
    return data}





}