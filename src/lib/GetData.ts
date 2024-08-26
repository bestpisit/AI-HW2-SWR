const fs = require('fs');

async function fetchAndConvertTSVtoJSON(url: string) {
    try {
        const response = await fetch(url);
        const tsvText = await response.text();
        const [headerLine, ...lines] = tsvText.split('\n').filter(line => line.trim() !== '');

        const data = lines.map(line => {
            const values = line.split('\t').map(normalizeString);
            return {
                s1: values.slice(0, 4), // First 4 values for station 1
                s2: values.slice(4, 8), // Next 4 values for station 2
                output: values[8]       // The 9th value as desire output
            };
        });

        return data;
    } catch (error) {
        console.error('Error fetching or converting TSV:', error);
    }
}

function normalizeString(input: string) {
    if (!input) return '';

    // Decode hexadecimal escape sequences
    let normalString = input.replace(/\\x([0-9A-Fa-f]{2})/g, (_, p1) => String.fromCharCode(parseInt(p1, 16)));

    // Remove null characters
    normalString = normalString.replace(/\x00/g, '');

    // Determine if the string is a float
    if (isFloat(normalString)) {
        return parseFloat(normalString);
    } else {
        return normalString;
    }
}

function isFloat(str: string) {
    return !isNaN(Number(str)) && !isNaN(parseFloat(str));
}

export async function GetData(url: string) {
    const data = await fetchAndConvertTSVtoJSON(url);
    fs.writeFileSync('data.json', JSON.stringify(data, null, 2)); // Pretty print JSON with 2 spaces
    console.log(data);
}
