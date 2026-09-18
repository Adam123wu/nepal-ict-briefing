const basePath = process.env.GITHUB_ACTIONS === 'true' ? '/nepal-ict-briefing' : '';
export default {output:'export',trailingSlash:true,images:{unoptimized:true},basePath};
