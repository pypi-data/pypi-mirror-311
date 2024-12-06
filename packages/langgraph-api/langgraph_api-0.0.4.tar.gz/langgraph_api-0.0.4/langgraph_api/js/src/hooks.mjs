// This hook is to ensure that @langchain/langgraph package
// found in /api folder has precendence compared to user-provided package
// found in /deps. Does not attempt to semver check for too old packages.
export async function resolve(specifier, context, nextResolve) {
  const parentURL = new URL("./graph.mts", import.meta.url).toString();

  if (specifier.startsWith("@langchain/langgraph")) {
    try {
      return nextResolve(specifier, { ...context, parentURL });
    } catch (error) {
      return nextResolve(specifier, context);
    }
  }

  return nextResolve(specifier, context);
}
