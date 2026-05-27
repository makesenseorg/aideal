/**
 * validate-and-comment.js
 * Validates dataset preferences.json and comments on PRs with results
 * 
 * Usage: Run from repo root during GitHub Actions workflow
 */

const fs = require('fs');
const path = require('path');

const VALID_CATEGORIES = [
  'genre-inclusion',
  'techno-solutionnisme',
  'vision-economique',
  'validisme-accessibilite',
  'inegalites-nord-sud',
  'ecologie-sobriete',
  'gouvernance-pouvoir-agir',
  'diversite-parcours'
];

function validateDataset() {
  const errors = [];
  const warnings = [];
  const seenIds = new Set();
  const categories = new Set();
  
  try {
    const dataPath = path.join(process.cwd(), 'dataset', 'preferences.json');
    const rawData = fs.readFileSync(dataPath, 'utf8');
    const data = JSON.parse(rawData);
    
    if (!Array.isArray(data)) {
      errors.push('preferences.json must be an array of entries');
      return { valid: false, errors, warnings, itemCount: 0, categories: 0 };
    }
    
    data.forEach((entry, index) => {
      const prefix = `Entry #${index + 1}`;
      
      if (!entry.id) {
        errors.push(`${prefix}: Missing id field`);
      } else if (seenIds.has(entry.id)) {
        errors.push(`${prefix}: Duplicate ID ${entry.id}`);
      } else {
        seenIds.add(entry.id);
      }
      
      if (!entry.category) {
        errors.push(`${prefix}: Missing category field`);
      } else if (!VALID_CATEGORIES.includes(entry.category)) {
        errors.push(`${prefix}: Invalid category ${entry.category}`);
      } else {
        categories.add(entry.category);
      }
      
      if (!entry.instruction || entry.instruction.trim() === '') {
        errors.push(`${prefix}: Missing or empty instruction field`);
      }
      
      if (!entry.chosen || entry.chosen.trim() === '') {
        errors.push(`${prefix}: Missing or empty chosen field`);
      }
      
      if (!entry.rejected || entry.rejected.trim() === '') {
        errors.push(`${prefix}: Missing or empty rejected field`);
      }
    });
    
    if (categories.size < 8) {
      warnings.push(`Dataset only covers ${categories.size}/8 categories`);
    }
    
    return {
      valid: errors.length === 0,
      errors,
      warnings,
      itemCount: data.length,
      categories: categories.size
    };
  } catch (e) {
    errors.push(`JSON parsing error: ${e.message}`);
    return { valid: false, errors, warnings: [], itemCount: 0, categories: 0 };
  }
}

function formatComment(result) {
  if (result.valid) {
    let comment = `### ✅ Dataset Validation Passed\n\n`;
    comment += `- **Entries**: ${result.itemCount}\n`;
    comment += `- **Categories covered**: ${result.categories}/8\n\n`;
    
    if (result.warnings.length > 0) {
      comment += '⚠️ **Warnings**:\n';
      result.warnings.forEach(w => comment += `- ${w}\n`);
      comment += '\n';
    }
    
    comment += '---\n';
    comment += 'This validation runs on every PR that modifies `dataset/preferences.json`.';
    return comment;
  } else {
    let comment = `### ❌ Dataset Validation Failed\n\n`;
    comment += '**Please fix the following errors before merging**:\n\n';
    result.errors.forEach(e => comment += `- ${e}\n`);
    
    if (result.warnings.length > 0) {
      comment += '\n⚠️ **Warnings** (non-blocking):\n';
      result.warnings.forEach(w => comment += `- ${w}\n`);
      comment += '\n';
    }
    
    comment += '---\n';
    comment += 'Please fix these issues and push your changes to update the validation status.';
    return comment;
  }
}

async function commentOnPR(result) {
  const isPR = process.env.GITHUB_EVENT_NAME === 'pull_request';
  
  if (!isPR) {
    console.log('Not a PR context, skipping comment');
    return;
  }
  
  try {
    // Write result to file for the GitHub Action step to use
    fs.writeFileSync('validation-result.json', JSON.stringify(result, null, 2));
    
    const { github } = require('@actions/github');
    const core = require('@actions/core');
    
    const octokit = github.getOctokit(process.env.GITHUB_TOKEN);
    
    const existingComments = await octokit.rest.issues.listComments({
      owner: process.env.GITHUB_REPOSITORY.split('/')[0],
      repo: process.env.GITHUB_REPOSITORY.split('/')[1],
      issue_number: parseInt(process.env.GITHUB_EVENT_NUMBER),
    });
    
    const validationComment = existingComments.data.find(c => 
      c.body && c.body.includes('Dataset Validation')
    );
    
    const commentBody = formatComment(result);
    
    if (validationComment) {
      await octokit.rest.issues.updateComment({
        owner: process.env.GITHUB_REPOSITORY.split('/')[0],
        repo: process.env.GITHUB_REPOSITORY.split('/')[1],
        comment_id: validationComment.id,
        body: commentBody,
      });
    } else {
      await octokit.rest.issues.createComment({
        owner: process.env.GITHUB_REPOSITORY.split('/')[0],
        repo: process.env.GITHUB_REPOSITORY.split('/')[1],
        issue_number: parseInt(process.env.GITHUB_EVENT_NUMBER),
        body: commentBody,
      });
    }
    
    console.log('Comment posted successfully');
  } catch (e) {
    console.error('Error posting comment:', e.message);
    // Non-fatal - validation still works without comment
  }
}

async function main() {
  console.log('Starting dataset validation...\n');
  
  const result = validateDataset();
  
  if (result.valid) {
    console.log('✅ Dataset validation passed');
    console.log(`Total entries: ${result.itemCount}`);
    console.log(`Categories covered: ${result.categories}/8`);
    if (result.warnings.length > 0) {
      console.log('Warnings:');
      result.warnings.forEach(w => console.log(` ⚠️  ${w}`));
    }
  } else {
    console.error('❌ Dataset validation failed');
    console.error('❌ ' + result.errors.join('\n❌ '));
    console.error('\nPlease fix the errors above before merging.');
  }
  
  await commentOnPR(result);
  
  if (!result.valid) {
    process.exit(1);
  }
}

main();
