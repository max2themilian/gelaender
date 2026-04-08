function renderTourDates(dates) {
  const list = document.getElementById("dates-list");
  if (!list) return;

  if (!dates.length) {
    list.innerHTML = '<li><span>New dates are being confirmed.</span></li>';
    return;
  }

  list.innerHTML = dates
    .map(
      (item) => `
      <li>
        <span>${item.date} | ${item.city} | ${item.venue_name}</span>
        <a href="${item.ticket_url}" target="_blank" rel="noopener noreferrer">Tickets</a>
      </li>
    `
    )
    .join("");
}

document.addEventListener("DOMContentLoaded", async () => {
  if (!window.GelaenderApi?.getTourDates) return;

  try {
    const dates = await window.GelaenderApi.getTourDates();
    renderTourDates(dates);
  } catch (error) {
    renderTourDates([]);
    console.error(error);
  }
});
