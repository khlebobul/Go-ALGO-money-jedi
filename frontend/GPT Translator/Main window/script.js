const companyItems = document.querySelectorAll(".company__list__item");
let chosenElemnt = companyItems[0];

chosenElemnt.classList.add("active");
companyItems.forEach(item => {
    item.addEventListener("click", function(){
        item.classList.add("active");
        item.style.transition = "all 1s";
        chosenElemnt.classList.remove("active");
        chosenElemnt = item;
    })
});

var xValues = [];
var yValues = [];
generateData("Math.sin(x)", 0, 10, 0.5);

new Chart("myChart", {
  type: "line",
  data: {
    labels: xValues,
    datasets: [{
      fill: false,
      pointRadius: 2,
      borderColor: "rgba(217, 240, 95, 1)",
      data: yValues
    }]
  },    
  options: {
    legend: {display: false},
    title: {
      display: true,
      fontSize: 16
    }
  }
});
function generateData(value, i1, i2, step = 1) {
  for (let x = i1; x <= i2; x += step) {
    yValues.push(eval(value));
    xValues.push(x);
  }
}