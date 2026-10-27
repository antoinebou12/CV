---
post_kind: conference
title: "Byzantium’s first workshop — Solidity and an ERC-20 token on Ethereum"
date: 2024-03-11T18:30:00-04:00
lastmod: 2026-10-24T16:00:00-04:00
description: "Byzantium’s first Ethereum workshop — Remix and Sepolia, OpenZeppelin ERC-20, deploy a token, and swap transfers with the room. Led by Khalil Anis Zabat."
translationKey: byzantium-solidity-ethereum-workshop
tags:
  - Byzantium
  - Solidity
  - Ethereum
  - Conference
  - Education
  - OpenZeppelin
  - ERC-20
images:
  - images/featured.png
---

![Byzantium workshop opening slide — Solidity on Ethereum, ÉTS classroom](./images/workshop-title-slide.png)

A quick recap of Byzantium’s **first Ethereum workshop**.

On **11 March 2024** at ÉTS, beginners and more advanced folks created and deployed their own token on-chain and transferred tokens to each other. Thanks to everyone who showed up — and to **Khalil Anis Zabat** for leading and organizing the session.



<!--more-->

We plan a follow-up with other token types and more advanced techniques. If you’d want a rerun — or you have ideas for the next workshops — say so in the comments on the LinkedIn thread (link below).

## What we actually did

The arc was deliberate and beginner-friendly:

1. **Remix in the browser** — compile and deploy without installing a full toolchain first, so you could redo the steps at home.
2. **A local dev setup** (editor + node tooling) — the “how professionals repeat this” half, with the same ERC-20 idea carried over.
3. **Sepolia** — test ETH from a faucet, **MetaMask** as the wallet, **Infura** (or similar) as the RPC bridge.
4. **OpenZeppelin** — don’t reinvent `transfer`; inherit battle-tested **ERC-20** and focus on name, symbol, decimals, and an initial mint.
5. **Peer transfers** — deploy, copy contract addresses, and **send tokens to each other** until the room felt like a tiny economy.

Until you push a transaction and see it on a block explorer, Solidity is just syntax. Afterward it is a public ledger with your address on one line.

## The token we started from

Khalil walked through a minimal mintable ERC-20 — roughly:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MyToken is ERC20 {
    constructor() ERC20("MyToken", "MTK") {
        _mint(msg.sender, 1000000 * 10 ** decimals());
    }
}
```

You pick **name** and **symbol**, set **decimals** (often 18), and **mint** an initial supply to `msg.sender` (the deployer). OpenZeppelin is the community’s shared library for standards — the same idea as **ERC-721** for NFTs, but here we stayed on fungible tokens.

![Live demo — editor and contract projected in the room](./images/demo-mytoken-vscode.png)

## Concepts that came up in Q&A

**Block explorers (Etherscan, Sepolia variants).** Every transaction is a row: who sent what, to whom, gas paid, block number.

**Gas and limits.** Contracts are not unconstrained Turing machines in practice — infinite loops can burn gas and stall. **Sepolia** kept the lesson affordable.

**ABI = the skeleton.** After deploy, the ABI is how apps (or bots) know which functions exist.

**On-chain vs off-chain data.** Storage on-chain is expensive. Patterns point to **hashes or URIs** for bulky data; the chain holds the reference.

## Room and energy

Tables, power strips, and laptops open — good for pairing when Remix threw a curveball or MetaMask asked for another confirmation.

![Participants after the workshop](./images/group-chalkboard.png)

![Room during the presentation](./images/audience-wide.png)

Byzantium framed **follow-up workshops** around other token types and deeper Solidity patterns. This one was the on-ramp.

## Links

- [LinkedIn thread / Byzantium recap](https://www.linkedin.com/posts/antoineboucher12_retour-sur-notre-tout-premier-workshop-activity-7173128307155156992-tQy4)
- [Deployed contract (short link)](https://lnkd.in/e-9T5-MX)
- [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts)
- [Remix IDE](https://remix.ethereum.org/)
- [Sepolia testnet explorer](https://sepolia.etherscan.io/)

Thanks to **Khalil** for teaching through the messy middle (wallets, faucets, failed txs), and to everyone who showed up for Byzantium’s first chain night.

## Related posts

- [Diagram prompts with ChatGPT and AIPRM]({{< ref "/posts/chatgpt-airprm-sequence-diagrams/index.md" >}}) — explaining systems in prose
- [QcES lean discovery pitch]({{< ref "/posts/qces-lean-discovery-pitch/index.md" >}}) — another ÉTS-adjacent learning format
