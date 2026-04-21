/**
 * /api/submit-pair endpoint
 * 
 * This is a placeholder for the GitHub API integration.
 * In production, you would use a serverless function (Vercel/AWS Lambda) with:
 * - GitHub OAuth app or personal access token in environment variables
 * - Repository: makesenseorg/aideal
 * - Branch: main
 * 
 * Required environment variable: GITHUB_TOKEN
 * 
 * Usage: POST /api/submit-pair
 * Body: { category, instruction, chosen, rejected, tags, source, reviewer_notes }
 */

// This file would be deployed as a serverless function
// For local development, you would use a proxy or mock

const GITHUB_REPO = 'makesenseorg/aideal';
const GITHUB_BRANCH = 'main';

async function submitPair(data) {
    // 1. Generate branch name
    const prefix = getCategoryPrefix(data.category);
    const branchName = `contrib/pair-${data.category}-${data.id}`;
    
    // 2. Fetch existing category file
    const categoryUrl = `https://api.github.com/repos/${GITHUB_REPO}/contents/dataset/categories/${data.category}.json?ref=${GITHUB_BRANCH}`;
    const categoryResponse = await fetch(categoryUrl, {
        headers: {
            'Authorization': `token ${process.env.GITHUB_TOKEN}`,
            'Accept': 'application/vnd.github.v3+json'
        }
    });
    
    if (!categoryResponse.ok) {
        throw new Error(`Failed to fetch category file: ${categoryResponse.status}`);
    }
    
    const categoryData = await categoryResponse.json();
    const pairs = JSON.parse(Buffer.from(categoryData.content, 'base64').toString());
    
    // 3. Check for duplicate ID
    const existingIds = pairs.map(p => p.id);
    if (existingIds.includes(data.id)) {
        throw new Error(`ID ${data.id} already exists in this category`);
    }
    
    // 4. Add new pair
    pairs.push(data);
    
    // 5. Create new commit
    const updatedContent = Buffer.from(JSON.stringify(pairs, null, 2)).toString('base64');
    const commitUrl = `https://api.github.com/repos/${GITHUB_REPO}/contents/dataset/categories/${data.category}.json`;
    
    const commitResponse = await fetch(commitUrl, {
        method: 'PUT',
        headers: {
            'Authorization': `token ${process.env.GITHUB_TOKEN}`,
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            message: `Add new pair: ${data.id}`,
            content: updatedContent,
            branch: GITHUB_BRANCH,
            sha: categoryData.sha
        })
    });
    
    if (!commitResponse.ok) {
        // Try with fork if direct commit fails
        throw new Error(`Failed to create commit: ${commitResponse.status}`);
    }
    
    // 6. Create PR (if in fork mode, would create PR from fork)
    // For MVP, just return success
    return {
        success: true,
        id: data.id,
        prUrl: `https://github.com/${GITHUB_REPO}/pull/NEW_PR_NUMBER`
    };
}

function getCategoryPrefix(category) {
    const prefixes = {
        "genre-inclusion": "genre",
        "techno-solutionnisme": "techno",
        "vision-economique": "eco",
        "validisme-accessibilite": "valid",
        "inegalites-nord-sud": "nord-sud",
        "ecologie-sobriete": "sobr",
        "gouvernance-pouvoir-agir": "gouv",
        "diversite-parcours": "diversite"
    };
    return prefixes[category] || category;
}

// Export for serverless deployment
module.exports = { submitPair, getCategoryPrefix };
