function main(necessity, pleasure, saving_month, investment_month, rent, vacation, funds, cashflow, expensable, expense_cash, expense_digital, expense_credit) {

  const remaining = parseInt(expensable) -
  (parseInt(expense_cash) + parseInt(expense_digital) + parseInt(expense_credit));
  if (remaining < 0) {
  window.alert("Expensable exceeded");
  }
  const xDoughnutExpense = ["expense_cash", "expense_digital", "expense_credit", "remaining"];
  const yDoughnutExpense = [ expense_cash,expense_digital, expense_credit, remaining ];
  const DoughnutExpenseColors = ["#ff96a4", "#ccffcc","#96bfff"];
  const xDoughnutBudget = ["necessity", "pleasure","saving_month", "investment_month",
                  "rent", "vacation", "funds", "cashflow"]
  const yDoughnutBudget = [
    necessity,
    pleasure,
    saving_month,
    investment_month,
    rent,
    vacation,
    funds,
    cashflow
  ]
  const DoughnutBudgetColors = [
    "#ff2929",
    "#0047c9",
    "#69ff7a",
    "pink",
    "#ff8e4d",
    "#73e3ff",
    "#9e3dff",
    "#fff878"
  ]

  new Chart("DoughnutExpense", {
  type: "doughnut",
  data: {
  labels: xDoughnutExpense,
  datasets: [{
  backgroundColor: DoughnutExpenseColors,
  data: yDoughnutExpense
  }]
  },
  options: {
  legend: {
      display: true,
      position: "right"
  },
  tooltips: {
      callbacks: {
          label: function(tooltipItem, data) {
              var label = data.labels[tooltipItem.index] || '';
              if (label) {
                  label += ': ';
              }
              var value = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
              label += value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") +
              " (" + (value / parseInt(expensable) * 100).toFixed(2) + " %)";
              return label;
          }
      }
  }
  }
  });

  new Chart("DoughnutBudget", {
  type: "doughnut",
  data: {
  labels: xDoughnutBudget,
  datasets: [{
  backgroundColor: DoughnutBudgetColors,
  data: yDoughnutBudget
  }]
  },
  options: {
  legend: {
      display: true,
      position: "right"
  },
  tooltips: {
      callbacks: {
          label: function(tooltipItem, data) {
              var label = data.labels[tooltipItem.index] || '';
              if (label) {
                  label += ': ';
              }
              var value = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
              label += value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") +
              " (" + (value / parseInt("{{ budget | safe }}") * 100).toFixed(2) + " %)";
              return label;
          }
      }
  }
  }
  });
}

function toggleText(elementId) {
const els = document.getElementsByClassName(elementId);
Object.entries(els).forEach(([ _, value]) => {
    if (!value.dataset.original) return;
    if (value.textContent === '********') {
        value.textContent = value.dataset.original;
    } else {
        value.textContent = '********';
    }
});
}