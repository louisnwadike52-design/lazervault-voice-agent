# Multilingual Voice Banking - Quick Reference

## Language Codes

| Language | Code | Flag | Speakers in Nigeria |
|----------|------|------|---------------------|
| English  | `en` | 🇬🇧   | 60M+ (official)     |
| Igbo     | `ig` | 🇳🇬   | 45M+ (Southeast)    |
| Hausa    | `ha` | 🇳🇬   | 85M+ (North)        |
| Yoruba   | `yo` | 🇳🇬   | 45M+ (Southwest)    |

---

## Common Commands by Language

### Send Money

| English | Igbo | Hausa | Yoruba |
|---------|------|-------|--------|
| Send 50 to John | Zie 50 nye John | Aika 50 zuwa John | Fi 50 ranṣẹ́ sí John |
| Transfer 100 | Nyefe 100 | Canja 100 | Gbé 100 |
| Send money | Zie ego | Aika kuɗi | Fi owó ranṣẹ́ |

### Confirmation

| English | Igbo | Hausa | Yoruba |
|---------|------|-------|--------|
| Yes | Ee | I | Bẹẹni |
| OK | Ọ dị mma | Lafiya | O daa |
| Confirm | Kwenye | Tabbatar | Jẹ́rìísí |
| Go ahead | Gaba n'ihu | Ci gaba | Tẹsíwájú |

### Cancellation

| English | Igbo | Hausa | Yoruba |
|---------|------|-------|--------|
| No | Mba | A'a | Bẹẹkọ |
| Cancel | Kagbuo | Soke | Fagile |
| Stop | Kwụsị | Tsaya | Dúró |
| Wait | Chere | Jira | Dúró dẹ |

### Status Responses

| English | Igbo | Hausa | Yoruba |
|---------|------|-------|--------|
| Done! | Emechara! | An gama! | Ti parí! |
| Failed | Ọdara | Ya kasa | Ó kùnà |
| Processing | Na-eme | Ana aiki | Ń ṣiṣẹ́ |
| Successful | Gara nke ọma | An yi nasara | Ṣe àṣeyọrí |

---

## Complete Example Flows

### 🇬🇧 ENGLISH
```
🤖: Who and how much?
👤: Send 50 to John
🤖: £50 to John Doe. Confirm?
👤: Yes
🤖: Done!
```

### 🇳🇬 IGBO
```
🤖: Onye na ole?
👤: Zie 50 nye John
🤖: 50 nye John Doe. Kwenye?
👤: Ee
🤖: Emechara!
```

### 🇳🇬 HAUSA
```
🤖: Wa da nawa?
👤: Aika 50 zuwa John
🤖: 50 zuwa John Doe. Tabbatar?
👤: I
🤖: An gama!
```

### 🇳🇬 YORUBA
```
🤖: Ta ni àti elo?
👤: Fi 50 ranṣẹ́ sí John
🤖: 50 sí John Doe. Jẹ́rìísí?
👤: Bẹẹni
🤖: Ti parí!
```

---

## Advanced Examples

### Transfer with Description

**English:**
```
👤: Send 100 to Sarah for rent
🤖: £100 to Sarah for rent. Confirm?
👤: Go
🤖: Done!
```

**Igbo:**
```
👤: Zie 100 nye Sarah maka ụlọ
🤖: 100 nye Sarah maka ụlọ. Kwenye?
👤: Gaa
🤖: Emechara!
```

**Hausa:**
```
👤: Aika 100 zuwa Sarah don haya
🤖: 100 zuwa Sarah don haya. Tabbatar?
👤: Je
🤖: An gama!
```

**Yoruba:**
```
👤: Fi 100 ranṣẹ́ sí Sarah fún ilé
🤖: 100 sí Sarah fún ilé. Jẹ́rìísí?
👤: Lọ
🤖: Ti parí!
```

---

### Multiple Recipients

**English:**
```
👤: Send 25 to John
🤖: 1. John Doe, 2. John Smith. Which number?
👤: 1
🤖: £25 to John Doe. Confirm?
👤: Yes
🤖: Done!
```

**Igbo:**
```
👤: Zie 25 nye John
🤖: 1. John Doe, 2. John Smith. Kedu nọmba?
👤: 1
🤖: 25 nye John Doe. Kwenye?
👤: Ee
🤖: Emechara!
```

**Hausa:**
```
👤: Aika 25 zuwa John
🤖: 1. John Doe, 2. John Smith. Wane lamba?
👤: 1
🤖: 25 zuwa John Doe. Tabbatar?
👤: I
🤖: An gama!
```

**Yoruba:**
```
👤: Fi 25 ranṣẹ́ sí John
🤖: 1. John Doe, 2. John Smith. Nọ́mbà wo?
👤: 1
🤖: 25 sí John Doe. Jẹ́rìísí?
👤: Bẹẹni
🤖: Ti parí!
```

---

### Error - Recipient Not Found

**English:**
```
👤: Send 75 to Xander
🤖: Can't find Xander. Spell it?
👤: X-A-N-D-E-R L-E-E
🤖: £75 to Xander Lee. Confirm?
👤: Yes
🤖: Done!
```

**Igbo:**
```
👤: Zie 75 nye Xander
🤖: Ahụghị m Xander. Sụpee ya?
👤: X-A-N-D-E-R L-E-E
🤖: 75 nye Xander Lee. Kwenye?
👤: Ee
🤖: Emechara!
```

**Hausa:**
```
👤: Aika 75 zuwa Xander
🤖: Ban same Xander ba. Rubuta shi?
👤: X-A-N-D-E-R L-E-E
🤖: 75 zuwa Xander Lee. Tabbatar?
👤: I
🤖: An gama!
```

**Yoruba:**
```
👤: Fi 75 ranṣẹ́ sí Xander
🤖: Mi ò rí Xander. Ṣe ìsípẹ́lì rẹ̀?
👤: X-A-N-D-E-R L-E-E
🤖: 75 sí Xander Lee. Jẹ́rìísí?
👤: Bẹẹni
🤖: Ti parí!
```

---

### Error - Transfer Failed

**English:**
```
👤: Send 1000 to Emma
🤖: £1000 to Emma Davis. Confirm?
👤: Yes
🤖: Failed. Try again?
👤: No
🤖: Cancelled.
```

**Igbo:**
```
👤: Zie 1000 nye Emma
🤖: 1000 nye Emma Davis. Kwenye?
👤: Ee
🤖: Ọdara. Nwaa ọzọ?
👤: Mba
🤖: Kagbuola.
```

**Hausa:**
```
👤: Aika 1000 zuwa Emma
🤖: 1000 zuwa Emma Davis. Tabbatar?
👤: I
🤖: Ya kasa. Ka sake gwadawa?
👤: A'a
🤖: An soke.
```

**Yoruba:**
```
👤: Fi 1000 ranṣẹ́ sí Emma
🤖: 1000 sí Emma Davis. Jẹ́rìísí?
👤: Bẹẹni
🤖: Ó kùnà. Gbìyànjú lẹ́ẹ̀kan sí i?
👤: Bẹẹkọ
🤖: Ti fagile.
```

---

## Banking Vocabulary

### Money Terms

| English | Igbo | Hausa | Yoruba |
|---------|------|-------|--------|
| Money | Ego | Kuɗi | Owó |
| Send | Zie / Nye | Aika | Fi ranṣẹ́ / Gbé |
| Transfer | Nyefe | Canja | Gbígbé |
| Amount | Ego / Ole | Adadi | Iye |
| Account | Akaụntụ | Asusun | Àkáwọ́ |

### Action Words

| English | Igbo | Hausa | Yoruba |
|---------|------|-------|--------|
| Confirm | Kwenye | Tabbatar | Jẹ́rìísí |
| Cancel | Kagbuo | Soke | Fagile |
| Wait | Chere | Jira | Dúró |
| Retry | Nwaa ọzọ | Sake gwadawa | Gbìyànjú lẹ́ẹ̀kan sí |
| Done | Emechara | An gama | Ti parí |

### Question Words

| English | Igbo | Hausa | Yoruba |
|---------|------|-------|--------|
| Who | Onye | Wa | Ta ni |
| How much | Ole | Nawa | Elo |
| Which | Kedu | Wane | Èwo |
| What | Gịnị | Me | Kí ni |
| When | Mgbe | Yaushe | Nígbà wo |

---

## Pronunciation Guide

### Igbo Special Characters
- **ị** = sounds like "i" in "pit"
- **ụ** = sounds like "u" in "put"
- **ọ** = sounds like "o" in "pot"
- **ṅ** = nasal "ng" sound
- **gb** = combined "g" and "b" sound

### Hausa Special Characters
- **ƙ** = emphatic "k" sound
- **ɗ** = implosive "d" sound
- **ɓ** = implosive "b" sound

### Yoruba Special Characters & Tones
- **ẹ** = sounds like "e" in "bet"
- **ọ** = sounds like "o" in "pot"
- **ṣ** = sounds like "sh"
- **á** = high tone
- **à** = low tone
- **ā** = mid tone

---

## Flutter Integration Snippet

```dart
// Quick integration example
void startVoiceBanking({required String languageCode}) {
  final metadata = jsonEncode({
    'access_token': userToken,
    'language': languageCode,  // 'en', 'ig', 'ha', 'yo'
  });

  // Connect to LiveKit with language preference
  liveKitClient.connect(
    url: livekitUrl,
    token: roomToken,
    roomOptions: RoomOptions(metadata: metadata),
  );
}

// Language selector UI
final languages = [
  {'code': 'en', 'name': 'English', 'flag': '🇬🇧'},
  {'code': 'ig', 'name': 'Igbo', 'flag': '🇳🇬'},
  {'code': 'ha', 'name': 'Hausa', 'flag': '🇳🇬'},
  {'code': 'yo', 'name': 'Yorùbá', 'flag': '🇳🇬'},
];
```

---

## Testing Checklist

### Per Language Tests

- [ ] **English**
  - [ ] Simple transfer: "Send 50 to John"
  - [ ] With description: "Send 100 for rent"
  - [ ] Multiple recipients
  - [ ] Not found error
  - [ ] Failed transfer
  - [ ] All confirmation words (yes, ok, sure, go)

- [ ] **Igbo**
  - [ ] Simple transfer: "Zie 50 nye John"
  - [ ] With description: "Zie 100 maka ụlọ"
  - [ ] Multiple recipients
  - [ ] Not found error
  - [ ] Failed transfer
  - [ ] All confirmation words (ee, ọ dị mma, kwenye, gaa)

- [ ] **Hausa**
  - [ ] Simple transfer: "Aika 50 zuwa John"
  - [ ] With description: "Aika 100 don haya"
  - [ ] Multiple recipients
  - [ ] Not found error
  - [ ] Failed transfer
  - [ ] All confirmation words (i, lafiya, tabbatar, je)

- [ ] **Yoruba**
  - [ ] Simple transfer: "Fi 50 ranṣẹ́ sí John"
  - [ ] With description: "Fi 100 fún ilé"
  - [ ] Multiple recipients
  - [ ] Not found error
  - [ ] Failed transfer
  - [ ] All confirmation words (bẹẹni, o daa, jerisi, lọ)

---

## Support

For issues or questions about multilingual support:
- 📧 Email: support@lazervault.com
- 📱 WhatsApp: +234-XXX-XXX-XXXX
- 🐛 GitHub: Report issues with language tag

**Nnọọ! (Igbo) / Sannu! (Hausa) / Ẹ káàbọ̀! (Yoruba) / Welcome!**
