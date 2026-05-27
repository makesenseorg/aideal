#!/usr/bin/env node
/**
 * Dataset Statistics Script
 * 
 * Displays quick dataset statistics: total pairs, pairs per category, sources breakdown.
 * 
 * Usage: node scripts/count_pairs.js
 */

const fs = require('fs');
const path = require('path');

function countPairs(baseDir) {
    const categoriesDir = path.join(baseDir, 'dataset', 'categories');
    
    if (!fs.existsSync(categoriesDir)) {
        console.error('Error: dataset/categories directory not found');
        process.exit(1);
    }
    
    const categories = [];
    const totalPairs = { count: 0, byCategory: {}, bySource: {} };
    
    // Read all category files
    const categoryFiles = fs.readdirSync(categoriesDir);
    
    for (const file of categoryFiles) {
        if (!file.endsWith('.json')) continue;
        
        const category = file.replace('.json', '');
        const filepath = path.join(categoriesDir, file);
        const pairs = JSON.parse(fs.readFileSync(filepath, 'utf8'));
        
        categories.push(category);
        totalPairs.byCategory[category] = pairs.length;
        totalPairs.count += pairs.length;
        
        // Count by source
        for (const pair of pairs) {
            const source = pair.source || 'unknown';
            totalPairs.bySource[source] = (totalPairs.bySource[source] || 0) + 1;
        }
    }
    
    // Sort categories alphabetically
    categories.sort();
    
    // Display statistics
    console.log('AIDEAL Dataset Statistics');
    console.log('========================\n');
    
    console.log(`Total: ${totalPairs.count} pairs\n`);
    
    console.log('By category:');
    const maxCategoryLen = Math.max(...categories.map(c => c.length));
    for (const category of categories) {
        const count = totalPairs.byCategory[category];
        const padding = ' '.repeat(maxCategoryLen - category.length);
        console.log(`  ${category}${padding}: ${count} pairs`);
    }
    
    console.log('\nBy source:');
    const maxSourceLen = Math.max(...Object.keys(totalPairs.bySource).map(s => s.length));
    for (const source of Object.keys(totalPairs.bySource).sort()) {
        const count = totalPairs.bySource[source];
        const padding = ' '.repeat(maxSourceLen - source.length);
        console.log(`  ${source}${padding}: ${count} pairs`);
    }
}

countPairs('.');
