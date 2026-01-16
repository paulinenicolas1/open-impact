const summaryText =
    "Analyse comparative approfondie des tendances climatiques et des précipitations observées de 1900 à 2025. Données basées sur les relevés historiques de Météo-France.";

const cityData = {
    Paris: {
        stationId: "Station ID · 71490",
        summary: summaryText,
        metrics: {},
    },
    Lyon: {
        stationId: "Station ID · 29821",
        summary: summaryText,
        metrics: {},
    },
    Marseille: {
        stationId: "Station ID · 55807",
        summary: summaryText,
        metrics: {},
    },
    Bordeaux: {
        stationId: "Station ID · 66342",
        summary: summaryText,
        metrics: {},
    },
};

const valeurTableau = {
    Paris: "paris",
    Brest: "brest",
    Lille: "lille",
    Bordeaux: "bordeaux",
    Lyon: "lyon",
    Marseille: "marseille",
};

const cityButtons = document.querySelectorAll(".city-btn");
const cityName = document.getElementById("city-name");
const stationId = document.getElementById("station-id");
const citySummary = document.getElementById("city-summary");
const metricNodes = document.querySelectorAll("[data-metric]");
const yearLabels = document.querySelectorAll("[data-year-label]");
const lastFullYear = Number.parseInt(new Date().getFullYear() - 1, 10);
const yearlyMetrics = new Map();

yearLabels.forEach((label) => {
    label.textContent = lastFullYear;
});

const formatNumber = (value, options) => {
    if (!Number.isFinite(value)) {
        return null;
    }
    return new Intl.NumberFormat("fr-FR", options).format(value);
};

const formatTemperature = (value) => {
    const formatted = formatNumber(value, {
        minimumFractionDigits: 1,
        maximumFractionDigits: 1,
    });
    return formatted ? `${formatted}°C` : "Donnée indisponible";
};

const formatRainfall = (value) => {
    const formatted = formatNumber(value, {
        maximumFractionDigits: 1,
    });
    return formatted ? `${formatted} mm` : "Donnée indisponible";
};

const parseCsvLine = (line, delimiter) => {
    const values = [];
    let current = "";
    let insideQuotes = false;

    for (let i = 0; i < line.length; i += 1) {
        const char = line[i];
        if (char === '"') {
            if (insideQuotes && line[i + 1] === '"') {
                current += '"';
                i += 1;
            } else {
                insideQuotes = !insideQuotes;
            }
            continue;
        }
        if (char === delimiter && !insideQuotes) {
            values.push(current);
            current = "";
            continue;
        }
        current += char;
    }
    values.push(current);
    return values;
};

const parseCsv = (text) => {
    const trimmed = text.trim();
    if (!trimmed) {
        return [];
    }
    const lines = trimmed.split(/\r?\n/);
    const headerLine = lines[0];
    const delimiter = headerLine.includes(";") && !headerLine.includes(",") ? ";" : ",";
    const headers = parseCsvLine(headerLine, delimiter).map((header) => header.trim());
    return lines.slice(1).map((line) => {
        const values = parseCsvLine(line, delimiter);
        const row = {};
        headers.forEach((header, index) => {
            row[header] = values[index];
        });
        return row;
    });
};

const toNumber = (value) => {
    if (value === undefined || value === null || value === "") {
        return null;
    }
    const numeric = Number(String(value).replace(",", "."));
    return Number.isFinite(numeric) ? numeric : null;
};

const loadYearlyMetrics = async () => {
    try {
        const response = await fetch("../data/output/final_yearly.csv");
        if (!response.ok) {
            return;
        }
        const text = await response.text();
        const rows = parseCsv(text);
        rows.forEach((row) => {
            const year = Number.parseInt(String(row.AAAA).trim(), 10);
            if (year !== lastFullYear) {
                return;
            }
            const cityKey = String(row.ville || "").trim();
            if (!cityKey) {
                return;
            }
            yearlyMetrics.set(cityKey, {
                avgTemp: toNumber(row.TMM),
                maxTemp: toNumber(row.TXAB),
                rainfall: toNumber(row.RR),
            });
        });
    } catch (error) {
        console.warn("Impossible de charger les métriques annuelles.", error);
    }
};

const getComputedMetrics = (city) => {
    const cityKey = valeurTableau[city];
    if (!cityKey) {
        return {};
    }
    const metrics = yearlyMetrics.get(cityKey);
    if (!metrics) {
        return {};
    }
    return {
        avgTemp: formatTemperature(metrics.avgTemp),
        maxTemp: formatTemperature(metrics.maxTemp),
        rainfall: formatRainfall(metrics.rainfall),
    };
};

const updateDashboard = (city) => {
    const data = cityData[city];
    if (!data) {
        return;
    }
    cityName.textContent = city;
    stationId.textContent = data.stationId;
    citySummary.textContent = data.summary;
    const baseMetrics = {
        avgTemp: "Donnée indisponible",
        avgTempChange: "Donnée indisponible",
        maxTemp: "Donnée indisponible",
        maxTempChange: "Donnée indisponible",
        rainfall: "Donnée indisponible",
        rainfallChange: "Donnée indisponible",
    };
    const metrics = {
        ...baseMetrics,
        ...data.metrics,
        ...getComputedMetrics(city),
    };
    metricNodes.forEach((node) => {
        const key = node.dataset.metric;
        node.textContent = metrics[key];
    });
};

loadYearlyMetrics().then(() => {
    updateDashboard(cityName.textContent);
});

cityButtons.forEach((button) => {
    button.addEventListener("click", () => {
        cityButtons.forEach((item) => {
            item.classList.remove("active");
            item.setAttribute("aria-pressed", "false");
        });
        button.classList.add("active");
        button.setAttribute("aria-pressed", "true");
        updateDashboard(button.dataset.city);
    });
});
