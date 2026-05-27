#!/usr/bin/env node
/**
 * validate_dataset.js — Vérifie le format et la cohérence du dataset AIDEAL
 * 
 * Usage :
 *   node scripts/validate_dataset.js                  # Valide toutes les catégories
 *   node scripts/validate_dataset.js --file <path>    # Valide un fichier spécifique
 * 
 * Codes de retour :
 *   0 — Validation réussie
 *   1 — Erreurs détectées
 */

const fs = require('fs');
const path = require('path');

const CATEGORIES_DIR = path.join(__dirname, '..', 'dataset', 'categories');
const REQUIRED_FIELDS = ['id', 'category', 'instruction', 'chosen', 'rejected', 'tags', 'source', 'date_added'];
const VALID_SOURCES = ['manual', 'openwebui-feedback', 'content-extraction', 'manual + enrichie avec références fondamentales'];
const VALID_CATEGORIES = [
  'genre-inclusion',
  'techno-solutionnisme',
  'vision-economique',
  'validisme-accessibilite',
  'inegalites-nord-sud',
  'ecologie-sobriete',
  'gouvernance-pouvoir-agir',
  'diversite-parcours',
];

function validatePair(pair, filename, index) {
  const errors = [];
  const prefix = `[${filename}][#${index}]`;

  // Champs obligatoires
  const missing = REQUIRED_FIELDS.filter(field => !(field in pair));
  if (missing.length > 0) {
    errors.push(`${prefix} Champs manquants : ${missing.join(', ')}`);
  }

  // Champs non vides
  for (const field of ['id', 'instruction', 'chosen', 'rejected']) {
    if (field in pair && !String(pair[field]).trim()) {
      errors.push(`${prefix} Le champ '${field}' est vide.`);
    }
  }

  // Source valide
  if ('source' in pair && !VALID_SOURCES.includes(pair['source'])) {
    errors.push(`${prefix} Source invalide : '${pair['source']}'. Valeurs acceptées : ${VALID_SOURCES.join(', ')}`);
  }

  // Catégorie valide
  if ('category' in pair && !VALID_CATEGORIES.includes(pair['category'])) {
    errors.push(`${prefix} Catégorie invalide : '${pair['category']}'.`);
  }

  // Tags est une liste
  if ('tags' in pair && !Array.isArray(pair['tags'])) {
    errors.push(`${prefix} Le champ 'tags' doit être un tableau.`);
  }

  // Chosen ≠ Rejected
  if ('chosen' in pair && 'rejected' in pair && pair['chosen'] === pair['rejected']) {
    errors.push(`${prefix} 'chosen' et 'rejected' sont identiques.`);
  }

  return errors;
}

function validateFile(filepath) {
  let content;
  try {
    content = fs.readFileSync(filepath, 'utf8');
  } catch (e) {
    return { pairs: 0, errors: [`[${path.basename(filepath)}] Impossible de lire le fichier : ${e.message}`] };
  }

  let data;
  try {
    data = JSON.parse(content);
  } catch (e) {
    return { pairs: 0, errors: [`[${path.basename(filepath)}] JSON invalide : ${e.message}`] };
  }

  if (!Array.isArray(data)) {
    return { pairs: 0, errors: [`[${path.basename(filepath)}] Le fichier doit contenir un tableau JSON à la racine.`] };
  }

  const errors = [];
  const seenIds = new Set();

  for (let i = 0; i < data.length; i++) {
    const pair = data[i];
    errors.push(...validatePair(pair, path.basename(filepath), i));

    // IDs uniques dans le fichier
    const pairId = pair.id;
    if (pairId) {
      if (seenIds.has(pairId)) {
        errors.push(`[${path.basename(filepath)}][#${i}] ID dupliqué : '${pairId}'`);
      }
      seenIds.add(pairId);
    }
  }

  return { pairs: data.length, errors };
}

function main() {
  const args = process.argv.slice(2);
  let filesToValidate;
  
  const fileIndex = args.indexOf('--file');
  if (fileIndex >= 0 && fileIndex + 1 < args.length) {
    filesToValidate = [path.resolve(args[fileIndex + 1])];
  } else {
    filesToValidate = fs.readdirSync(CATEGORIES_DIR)
      .filter(f => f.endsWith('.json'))
      .map(f => path.join(CATEGORIES_DIR, f))
      .sort();
  }

  let totalPairs = 0;
  const totalErrors = [];

  for (const filepath of filesToValidate) {
    const result = validateFile(filepath);
    totalPairs += result.pairs;
    totalErrors.push(...result.errors);
    
    const status = result.errors.length > 0 
      ? `${result.errors.length} erreur(s)` 
      : 'OK';
    console.log(`  ${path.basename(filepath).padEnd(45)} ${result.pairs.toString().padStart(4)} paire(s)  [${status}]`);
  }

  console.log(`\nTotal : ${totalPairs} paire(s) dans ${filesToValidate.length} fichier(s)`);

  if (totalErrors.length > 0) {
    console.log(`\n${totalErrors.length} erreur(s) détectée(s) :\n`);
    totalErrors.forEach(error => console.log(`  ✗ ${error}`));
    process.exit(1);
  } else {
    console.log('\nValidation réussie.');
    process.exit(0);
  }
}

main();
