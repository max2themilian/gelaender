const API_BASE = "http://127.0.0.1:8000/api";

async function fetchJson(path) {
  const response = await fetch(`${API_BASE}${path}`);
  if (!response.ok) throw new Error(`API request failed: ${response.status}`);
  return response.json();
}

async function getProducts() {
  return fetchJson("/products");
}

async function getTourDates() {
  return fetchJson("/tour-dates");
}

async function getSocialLinks() {
  return fetchJson("/social-links");
}

window.GelaenderApi = {
  getProducts,
  getTourDates,
  getSocialLinks,
};
