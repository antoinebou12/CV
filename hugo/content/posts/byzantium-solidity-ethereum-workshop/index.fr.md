---
post_kind: conference
title: "Premier atelier Byzantium — Solidity et token ERC-20 sur Ethereum"
date: 2024-03-11T18:30:00-04:00
description: "Retour sur le premier workshop Byzantium sur Ethereum : contrat ERC-20 avec OpenZeppelin, déploiement et échanges entre participants."
translationKey: byzantium-solidity-ethereum-workshop
tags:
    - Solidity
    - Ethereum
    - ERC-20
    - OpenZeppelin
    - Blockchain
    - Conference
    - Education
    - Byzantium
images:
    - featured.png
---

Lundi, **Byzantium** a organisé son **premier atelier sur Ethereum** : une session accessible aux débutant·e·s comme aux personnes déjà à l’aise avec la blockchain, avec mise en pratique jusqu’au **déploiement d’un token** et des **transferts entre portefeuilles**.

![Diapositive d’ouverture — Workshop sur Solidity (Ethereum)](./images/workshop-title-slide.png)

## Programme

L’animation, assurée par **Khalil Anis Zabat**, est partie d’une base **Solidity** et d’un contrat **ERC-20** standard, en s’appuyant sur **OpenZeppelin** : définir le nom et le symbole du token, fixer les **décimales**, et **émettre** une première quantité pour le déployeur. Ensuite, chacun·e a pu suivre la démo, déployer son propre contrat sur un réseau de test, puis **échanger des tokens** avec les autres participant·e·s — le passage concret du « code sur l’écran » à « quelque chose qu’on peut envoyer à un pair ».

![Démo — MyToken.sol dans l’éditeur](./images/demo-mytoken-vscode.png)

Le squelette montré pendant l’atelier ressemblait à ceci (contrat minimal ERC-20 + mint initial) :

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

## Ambiance et suite

La salle, format tables et prises intégrées, se prêtait bien au **pair programming** et aux allers-retours avec l’animateur. L’objectif annoncé pour la suite : d’autres ateliers sur **d’autres types de tokens** et des **techniques plus avancées**.

![Quelques participant·e·s après l’atelier](./images/group-chalkboard.png)

![Salle pendant la présentation](./images/audience-wide.png)

## Liens

- **Contexte et annonce** (repost Byzantium, fil LinkedIn) : [publication associée](https://www.linkedin.com/posts/antoineboucher12_retour-sur-notre-tout-premier-workshop-activity-7173128307155156992-tQy4).
- **Mon contrat déployé** (lien court ; redirige vers l’explorateur du contrat) : [lnkd.in/e-9T5-MX](https://lnkd.in/e-9T5-MX).

Merci à **Khalil** pour l’organisation et la pédagogie, et à **Byzantium** ainsi qu’aux participant·e·s pour cette première édition.

**[Version courte en anglais]({{< ref "/posts/byzantium-solidity-ethereum-workshop/index.md" >}})** — même slug ; vous pouvez aussi passer en **EN** depuis l’en-tête du site.
