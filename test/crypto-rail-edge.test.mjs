import assert from "node:assert/strict";
import { describe, it } from "node:test";
import { PostQuantumCryptoRail } from "../src/crypto-rail.mjs";

describe("PQC rail edges", () => {
  it("optIn must be boolean true, path traversal still cannot touch v0", () => {
    const sneaky = new PostQuantumCryptoRail({ optIn: "true" });
    assert.equal(sneaky.encapsulate().code, "OPT_IN_REQUIRED");
    const on = new PostQuantumCryptoRail({ optIn: true });
    assert.equal(on.write("../schema/juge.v0.json").code, "IMMUTABLE_V0");
    assert.equal(on.write("schema/juge.v0.json\0.md").code, "IMMUTABLE_V0");
    assert.equal(on.write("").code, "AI_WRITE_DENIED");
  });
});
