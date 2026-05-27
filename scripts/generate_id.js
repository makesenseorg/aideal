#!/usr/bin/env node
/**
 * Pair ID Generator - Node.js version
 * 
 * Generates the next available pair ID following the `category-###` convention.
 * 
 * Usage: node scripts/generate_id.js --category <category-name>
 * 
 * Category names:
 * - genre-inclusion -> genre-041
 * - techno-solutionnisme -> techno-039
 * - vision-economique -> eco-039
 * - validisme-accessibilite -> valid-039
 * - inegalites-nord-sud -> nord-sud-041
 * - ecologie-sobriete -> sobr-040
 * - gouvernance-pouvoir-agir -> gouv-040
 * - diversite-parcours -> diversite-040
 */

const fs = require('fs');
const path = require('path');

// Map from full category name to ID prefix
const CATEGORY_PREFIXES = {
    "genre-inclusion": "genre",
    "techno-solutionnisme": "techno",
    "vision-economique": "eco",
    "validisme-accessibilite": "valid",
    "inegalites-nord-sud": "nord-sud",
    "ecologie-sobriete": "sobr",
    "gouvernance-pouvoir-agir": "gouv",
    "diversite-parcours": "diversite",
};

function parseArgs(args) {
    const result = { category: null, baseDir: '.' };
    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--category' || args[i] === '-c') {
            result.category = args[++i];
        } else if (args[i] === '--base-dir' || args[i] === '-d') {
            result.baseDir = args[++i];
        }
    }
    return result;
}

function loadCategoryFile(category, baseDir) {
    const filepath = path.join(baseDir, 'dataset', 'categories', `${category}.json`);
    if (!fs.existsSync(filepath)) {
        throw new Error(`Category file not found: ${filepath}`);
    }
    const content = fs.readFileSync(filepath, 'utf8');
    return JSON.parse(content);
}

function getNextIdForCategory(category, baseDir) {
    const prefix = CATEGORY_PREFIXES[category];
    
    if (!prefix) {
        throw new Error(`Unknown category: ${category}. Available categories: ${Object.keys(CATEGORY_PREFIXES).join(', ')}`);
    }
    
    // Load existing pairs in this category
    const pairs = loadCategoryFile(category, baseDir);
    
    // Find the max number for this prefix in the category
    let maxNum = 0;
    for (const pair of pairs) {
        const pairId = pair.id || '';
        if (pairId.startsWith(prefix + '-')) {
            const numPart = pairId.split('-')[1];
            const num = parseInt(numPart, 10);
            if (!isNaN(num)) {
                maxNum = Math.max(maxNum, num);
            }
        }
    }
    
    const nextNum = maxNum + 1;
    return `${prefix}-${nextNum.toString().padStart(3, '0')}`;
}

function main() {
    const args = parseArgs(process.argv.slice(2));
    
    if (!args.category) {
        console.error('Error: --category is required');
        console.error('Usage: node generate_id.js --category <category-name>');
        console.error('Available categories: genre-inclusion, techno-solutionnisme, vision-economique, validisme-accessibilite, inegalites-nord-sud, ecologie-sobriete, gouvernance-pouvoir-agir, diversite-parcours');
        process.exit(1);
    }
    
    const baseDir = path.resolve(args.baseDir);
    
    try {
        const nextId = getNextIdForCategory(args.category, baseDir);
        console.log(nextId);
        process.exit(0);
    } catch (error) {
        console.error(`Error: ${error.message}`);
        process.exit(1);
    }
}

main();
