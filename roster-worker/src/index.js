const REPO_OWNER = "thepusoproject";
const REPO_NAME = "tpp-sari-sari-store";

function corsHeaders(origin) {
  return {
    "Access-Control-Allow-Origin": origin || "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
  };
}

function normalizeRepo(value) {
  if (!value) {
    throw new Error("Missing repo");
  }
  let repo = value.trim();
  if (repo.startsWith("http://") || repo.startsWith("https://")) {
    try {
      const url = new URL(repo);
      repo = url.pathname.replace(/^\//, "");
    } catch (err) {
      throw new Error("Invalid repo URL");
    }
  }
  if (!repo.includes("/")) {
    throw new Error("Repo must be owner/name");
  }
  return repo;
}

function buildIssueBody(handle, repo, notes) {
  return [
    "### Roster signup",
    `- GitHub handle: ${handle}`,
    `- Repo: ${repo}`,
    `- Notes: ${notes || '—'}`,
  ].join("\n");
}

async function createIssue(payload, env) {
  const apiUrl = `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/issues`;
  const resp = await fetch(apiUrl, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${env.GITHUB_TOKEN}`,
      "Content-Type": "application/json",
      Accept: "application/vnd.github+json",
      "User-Agent": "tpp-roster-worker",
    },
    body: JSON.stringify(payload),
  });
  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(`GitHub API error (${resp.status}): ${text}`);
  }
  return resp.json();
}

export default {
  async fetch(request, env) {
    const headers = corsHeaders(env.ALLOWED_ORIGIN);

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers });
    }

    if (request.method !== "POST") {
      return new Response("Not found", { status: 404, headers });
    }

    let data;
    try {
      data = await request.json();
    } catch (err) {
      return new Response(JSON.stringify({ error: "Invalid JSON payload" }), {
        status: 400,
        headers: { ...headers, "Content-Type": "application/json" },
      });
    }

    const handle = (data.handle || "").trim();
    const repoInput = (data.repo || "").trim();
    const notes = (data.notes || "").trim();

    if (!handle) {
      return new Response(JSON.stringify({ error: "Missing GitHub handle" }), {
        status: 400,
        headers: { ...headers, "Content-Type": "application/json" },
      });
    }
    if (!repoInput) {
      return new Response(JSON.stringify({ error: "Missing repo" }), {
        status: 400,
        headers: { ...headers, "Content-Type": "application/json" },
      });
    }

    let repo;
    try {
      repo = normalizeRepo(repoInput);
    } catch (err) {
      return new Response(JSON.stringify({ error: err.message }), {
        status: 400,
        headers: { ...headers, "Content-Type": "application/json" },
      });
    }

    const title = `Roster signup: ${handle}`;
    const body = buildIssueBody(handle, repo, notes);

    try {
      const issue = await createIssue({ title, body }, env);
      return new Response(JSON.stringify({ status: "ok", issue_url: issue.html_url }), {
        status: 200,
        headers: { ...headers, "Content-Type": "application/json" },
      });
    } catch (err) {
      return new Response(JSON.stringify({ error: err.message }), {
        status: 502,
        headers: { ...headers, "Content-Type": "application/json" },
      });
    }
  },
};
