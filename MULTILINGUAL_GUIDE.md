# LazerVault Multilingual Voice Banking Guide

## Overview

LazerVault Voice Agent now supports **4 languages** to enable users across Nigeria to make banking transactions in their native languages:

1. 🇬🇧 **English** (en)
2. 🇳🇬 **Igbo** (ig)
3. 🇳🇬 **Hausa** (ha)
4. 🇳🇬 **Yoruba** (yo)

Users can now say "Send 50 to John" in English, "Zie 50 nye John" in Igbo, "Aika 50 zuwa John" in Hausa, or "Fi 50 ranṣẹ́ sí John" in Yoruba!

---

## Features

### ✅ Multilingual Speech Recognition (STT)
- **Technology**: OpenAI Whisper
- **Supports**: Igbo, Hausa, Yoruba, and 50+ other languages
- **Auto-detection**: Automatically detects which language the user is speaking
- **Accuracy**: High accuracy for Nigerian English accents and local languages

### ✅ Multilingual AI Understanding (LLM)
- **Technology**: OpenAI GPT-4o
- **Capabilities**: Understands banking commands in all 4 languages
- **Context-aware**: Maintains conversation context across language switches
- **Natural**: Responds in the same language the user speaks

### ✅ Multilingual Text-to-Speech (TTS)
- **Technology**: OpenAI TTS (Alloy voice)
- **Output**: Speaks responses in user's chosen language
- **Quality**: Clear pronunciation for English and reasonable quality for Nigerian languages

### ✅ Optimized Conversations
- All 4 languages use the **same fast, optimized conversation flow**
- 3-6 word responses in each language
- Express mode available in all languages
- Natural affirmative words accepted (e.g., "ee" in Igbo, "i" in Hausa, "bẹẹni" in Yoruba)

---

## Supported Languages in Detail

### 1. English (en)

**Example Conversation:**
```
🤖 Agent: "Who and how much?"
👤 User: "Send 50 to Sarah"
🤖 Agent: "£50 to Sarah Johnson. Confirm?"
👤 User: "Yes"
🤖 Agent: "Done!"
```

**Confirmation words:** yes, yep, ok, sure, confirm, go, proceed

---

### 2. Igbo (ig)

**Ọmụmaatụ Mkparịta Ụka (Example Conversation):**
```
🤖 Agent: "Onye na ole?"
👤 Onye ọrụ: "Zie 50 nye Sarah"
🤖 Agent: "50 nye Sarah Johnson. Kwenye?"
👤 Onye ọrụ: "Ee"
🤖 Agent: "Emechara!"
```

**Okwu nkwenye (Confirmation words):** ee, ọ dị mma, n'ezie, kwenye, gaa, gaba n'ihu

**Common Banking Phrases:**
- "Zie ego" / "Nye" = Send money
- "Emechara" = Done
- "Ọdara" = Failed
- "Kagbuola" = Cancelled
- "Kwenye" = Confirm

---

### 3. Hausa (ha)

**Misali Tattaunawa (Example Conversation):**
```
🤖 Agent: "Wa da nawa?"
👤 Mai amfani: "Aika 50 zuwa Sarah"
🤖 Agent: "50 zuwa Sarah Johnson. Tabbatar?"
👤 Mai amfani: "I"
🤖 Agent: "An gama!"
```

**Kalmomin tabbatarwa (Confirmation words):** i, eh, to, lafiya, tabbatar, je, ci gaba

**Common Banking Phrases:**
- "Aika kuɗi" / "Canja kuɗi" = Send money
- "An gama" = Done
- "Ya kasa" = Failed
- "An soke" = Cancelled
- "Tabbatar" = Confirm

---

### 4. Yoruba (yo)

**Àpẹẹrẹ Ìjíròrò (Example Conversation):**
```
🤖 Agent: "Ta ni àti elo?"
👤 Olùmúlò: "Fi 50 ranṣẹ́ sí Sarah"
🤖 Agent: "50 sí Sarah Johnson. Jẹ́rìísí?"
👤 Olùmúlò: "Bẹẹni"
🤖 Agent: "Ti parí!"
```

**Àwọn ọ̀rọ̀ ìjẹ́rìísí (Confirmation words):** bẹẹni, o daa, daju, jerisi, lọ, tẹsiwaju

**Common Banking Phrases:**
- "Fi owó ranṣẹ́" = Send money
- "Ti parí" = Done
- "Ó kùnà" = Failed
- "Ti fagile" = Cancelled
- "Jẹ́rìísí" = Confirm

---

## How It Works

### Language Selection

The voice agent determines which language to use through the **room metadata** sent from your Flutter app:

```dart
// Flutter example
final metadata = {
  'access_token': userToken,
  'language': 'ig'  // 'en', 'ig', 'ha', or 'yo'
};
```

### Language Detection Flow

1. **User opens app** → Selects preferred language in settings
2. **Flutter app** → Sends language code in LiveKit room metadata
3. **Voice agent** → Initializes with user's language
4. **Greeting** → Agent greets user in their language
5. **Conversation** → All responses in user's language
6. **Whisper STT** → Recognizes speech in that language
7. **GPT-4** → Understands and responds in that language
8. **TTS** → Speaks response back in that language

### Automatic Language Detection

Even if no language is specified, Whisper can auto-detect:
- User speaks in Yoruba
- Whisper STT detects it's Yoruba
- GPT-4 responds in Yoruba
- Conversation continues in Yoruba

---

## Integration Guide

### Flutter App Integration

#### 1. Add Language Selector to Settings

```dart
// In your settings page
enum VoiceBankingLanguage {
  english('en', 'English'),
  igbo('ig', 'Igbo'),
  hausa('ha', 'Hausa'),
  yoruba('yo', 'Yorùbá');

  final String code;
  final String name;

  const VoiceBankingLanguage(this.code, this.name);
}

class LanguageSelector extends StatelessWidget {
  final VoiceBankingLanguage selectedLanguage;
  final Function(VoiceBankingLanguage) onLanguageChanged;

  @override
  Widget build(BuildContext context) {
    return DropdownButton<VoiceBankingLanguage>(
      value: selectedLanguage,
      items: VoiceBankingLanguage.values.map((lang) {
        return DropdownMenuItem(
          value: lang,
          child: Text('${_getFlag(lang)} ${lang.name}'),
        );
      }).toList(),
      onChanged: (lang) {
        if (lang != null) onLanguageChanged(lang);
      },
    );
  }

  String _getFlag(VoiceBankingLanguage lang) {
    switch (lang) {
      case VoiceBankingLanguage.english:
        return '🇬🇧';
      case VoiceBankingLanguage.igbo:
      case VoiceBankingLanguage.hausa:
      case VoiceBankingLanguage.yoruba:
        return '🇳🇬';
    }
  }
}
```

#### 2. Pass Language to LiveKit Session

```dart
// When starting voice banking session
Future<void> startVoiceBankingSession({
  required String accessToken,
  required VoiceBankingLanguage language,
}) async {
  final metadata = jsonEncode({
    'access_token': accessToken,
    'language': language.code,  // 'en', 'ig', 'ha', or 'yo'
  });

  // Create LiveKit room with metadata
  final room = await liveKitClient.connect(
    url: livekitUrl,
    token: roomToken,
    roomOptions: RoomOptions(
      metadata: metadata,
    ),
  );
}
```

#### 3. Display Language-Specific UI

```dart
// Show appropriate instructions based on language
String getVoiceBankingInstructions(VoiceBankingLanguage language) {
  switch (language) {
    case VoiceBankingLanguage.english:
      return 'Say "Send [amount] to [name]" to transfer money';
    case VoiceBankingLanguage.igbo:
      return 'Kwuo "Zie [ego] nye [aha]" iji nyefe ego';
    case VoiceBankingLanguage.hausa:
      return 'Ka ce "Aika [kuɗi] zuwa [suna]" don canja kuɗi';
    case VoiceBankingLanguage.yoruba:
      return 'Sọ "Fi [owó] ranṣẹ́ sí [orúkọ]" láti gbé owó';
  }
}
```

#### 4. Handle Transfer Completion in All Languages

```dart
// Listen for transfer completion
liveKitRoom.on<DataReceivedEvent>((event) {
  if (event.topic == 'flutter_updates') {
    final data = jsonDecode(event.data);

    if (data['event'] == 'transfer_completed') {
      final transaction = data['data'];

      // Show success message in user's language
      _showSuccessMessage(
        language: currentLanguage,
        transaction: transaction,
      );
    }
  }
});

void _showSuccessMessage({
  required VoiceBankingLanguage language,
  required Map<String, dynamic> transaction,
}) {
  final messages = {
    VoiceBankingLanguage.english: 'Transfer successful!',
    VoiceBankingLanguage.igbo: 'Nyefe gara nke ọma!',
    VoiceBankingLanguage.hausa: 'An yi nasarar canja kuɗi!',
    VoiceBankingLanguage.yoruba: 'Gbígbé owó ṣe àṣeyọrí!',
  };

  ScaffoldMessenger.of(context).showSnackBar(
    SnackBar(content: Text(messages[language]!)),
  );
}
```

---

## Testing Multilingual Support

### Test Scenarios for Each Language

#### English Test Cases
```
✅ "Send 50 to John"
✅ "Transfer 100 to Sarah for rent"
✅ "Send 25 to Mike tomorrow"
✅ Confirm with: "yes", "ok", "sure", "go"
```

#### Igbo Test Cases
```
✅ "Zie 50 nye John"
✅ "Nyefe 100 nye Sarah maka ụlọ"
✅ "Zie 25 nye Mike echi"
✅ Kwenye na: "ee", "ọ dị mma", "gaa"
```

#### Hausa Test Cases
```
✅ "Aika 50 zuwa John"
✅ "Canja 100 zuwa Sarah don haya"
✅ "Aika 25 zuwa Mike gobe"
✅ Tabbatar da: "i", "lafiya", "je"
```

#### Yoruba Test Cases
```
✅ "Fi 50 ranṣẹ́ sí John"
✅ "Gbé 100 sí Sarah fún ilé"
✅ "Fi 25 ranṣẹ́ sí Mike lọ́la"
✅ Jẹ́rìísí pẹ̀lú: "bẹẹni", "o daa", "lọ"
```

### Running Tests

```bash
# Test language module
python3 -c "from languages import *; print('Testing all languages:');
for lang in Language:
    print(f'{lang.value}: {get_greeting(lang)}')"

# Start agent with specific language (for testing)
python3 main.py
# Then connect with metadata: {"language": "ig"}
```

---

## Technical Implementation

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Flutter App                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  Language Selector: en / ig / ha / yo          │    │
│  └────────────────────┬───────────────────────────┘    │
└───────────────────────┼─────────────────────────────────┘
                        │ Metadata: {language: "ig"}
                        ▼
┌─────────────────────────────────────────────────────────┐
│              LiveKit Voice Agent (Python)               │
│  ┌──────────────────────────────────────────────────┐  │
│  │  1. Parse metadata → Extract language code       │  │
│  │  2. Initialize agent with user's language        │  │
│  │  3. Load language-specific instructions         │  │
│  │  4. Configure STT with language hint             │  │
│  │  5. Greet in user's language                     │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│   Whisper   │ │   GPT-4o    │ │ OpenAI TTS  │
│     STT     │ │     LLM     │ │   (Alloy)   │
│             │ │             │ │             │
│  Supports:  │ │  Supports:  │ │  Supports:  │
│  • English  │ │  • English  │ │  • English  │
│  • Igbo     │ │  • Igbo     │ │  • Multi*   │
│  • Hausa    │ │  • Hausa    │ │             │
│  • Yoruba   │ │  • Yoruba   │ │             │
└─────────────┘ └─────────────┘ └─────────────┘

* TTS quality varies by language
```

### Language Module Structure

```
languages.py
│
├── Language (Enum)
│   ├── ENGLISH = "en"
│   ├── IGBO = "ig"
│   ├── HAUSA = "ha"
│   └── YORUBA = "yo"
│
├── GREETINGS (Dict)
│   └── Quick greetings in each language
│
├── AGENT_INSTRUCTIONS (Dict)
│   └── Full banking instructions translated
│
├── CONFIRMATION_WORDS (Dict)
│   └── Affirmative words in each language
│
├── CANCELLATION_WORDS (Dict)
│   └── Negative words in each language
│
├── COMMON_PHRASES (Dict)
│   └── Banking phrases (done, failed, etc.)
│
└── Helper Functions
    ├── detect_language_from_text()
    ├── get_greeting()
    ├── get_instructions()
    ├── get_phrase()
    ├── is_confirmation()
    └── is_cancellation()
```

---

## Model Selection & Performance

### Speech-to-Text (STT)

**Model:** OpenAI Whisper (`whisper-1`)

**Performance by Language:**
| Language | Accuracy | Speed | Notes |
|----------|----------|-------|-------|
| English  | ★★★★★ | Fast | Excellent for Nigerian English accents |
| Igbo     | ★★★★☆ | Fast | Very good, trained on African languages |
| Hausa    | ★★★★☆ | Fast | Very good, widely spoken |
| Yoruba   | ★★★★☆ | Fast | Very good, common in West Africa |

**Configuration:**
```python
stt=openai.STT(
    model="whisper-1",
    language=user_language.value  # 'en', 'ig', 'ha', 'yo'
)
```

### Language Model (LLM)

**Model:** OpenAI GPT-4o (`gpt-4o`)

**Why GPT-4o:**
- Better multilingual understanding than GPT-3.5
- Faster than GPT-4 Turbo
- More cost-effective for production
- Good support for African languages

**Performance by Language:**
| Language | Understanding | Response Quality | Cost |
|----------|---------------|------------------|------|
| English  | ★★★★★ | Excellent | Standard |
| Igbo     | ★★★★☆ | Good | Standard |
| Hausa    | ★★★★☆ | Good | Standard |
| Yoruba   | ★★★★☆ | Good | Standard |

**Configuration:**
```python
llm=openai.LLM(
    model="gpt-4o",
    temperature=0.7  # Slightly higher for natural multilingual responses
)
```

### Text-to-Speech (TTS)

**Model:** OpenAI TTS (`tts-1`)
**Voice:** Alloy

**Why Alloy Voice:**
- Most neutral accent
- Works reasonably well across languages
- Clear pronunciation
- Good for African language phonetics

**Performance by Language:**
| Language | Pronunciation | Naturalness | Notes |
|----------|---------------|-------------|-------|
| English  | ★★★★★ | Excellent | Native-quality |
| Igbo     | ★★★☆☆ | Fair | Acceptable, some tonal issues |
| Hausa    | ★★★★☆ | Good | Clear, understandable |
| Yoruba   | ★★★☆☆ | Fair | Diacritics not always perfect |

**Configuration:**
```python
tts=openai.TTS(
    voice="alloy",
    model="tts-1"
)
```

**Future Improvements:**
For better TTS quality in Nigerian languages, consider:
- Google Cloud TTS (has Yoruba support: `yo-NG`)
- Azure TTS (has Hausa support: `ha-Latn-NG`)
- Custom voice cloning services

---

## Cost Considerations

### Per-Transaction Costs (Approximate)

**English Transaction:**
- STT (Whisper): $0.006 per minute → ~$0.003 for 30 sec
- LLM (GPT-4o): $0.015 per 1k tokens → ~$0.006 for transfer
- TTS: $0.015 per 1k chars → ~$0.002 for responses
- **Total: ~$0.011 per transaction**

**Nigerian Languages (Igbo/Hausa/Yoruba):**
- STT (Whisper): Same as English → ~$0.003
- LLM (GPT-4o): Slightly more tokens → ~$0.008
- TTS: Same as English → ~$0.002
- **Total: ~$0.013 per transaction**

**Monthly Cost Estimates:**
| Users | Transactions/Month | Cost (English) | Cost (Nigerian Lang) |
|-------|-------------------|----------------|---------------------|
| 100   | 1,000            | $11           | $13                 |
| 1,000 | 10,000           | $110          | $130                |
| 10,000| 100,000          | $1,100        | $1,300              |

**Optimization Tips:**
- Cache common responses
- Use response streaming for faster perceived speed
- Implement voice activity detection to minimize STT costs
- Consider switching to GPT-4o-mini for cost-sensitive deployments ($0.003/1k tokens)

---

## Troubleshooting

### Issue: Wrong Language Detected

**Symptom:** Agent responds in wrong language despite metadata setting

**Solutions:**
1. Verify metadata is being sent correctly:
```dart
print('Metadata sent: $metadata');
```

2. Check agent logs:
```bash
# Look for language initialization logs
tail -f logs/voice-agent.log | grep "language"
```

3. Ensure language code is valid (`en`, `ig`, `ha`, `yo`)

---

### Issue: Poor TTS Pronunciation

**Symptom:** TTS mispronounces Nigerian language words

**Solutions:**
1. **For Igbo/Yoruba**: Consider adding phonetic spelling
2. **For Hausa**: Current TTS should work well
3. **Alternative**: Implement Google Cloud TTS for better Nigerian language support

```python
# Future enhancement: Google Cloud TTS
from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()

voice = texttospeech.VoiceSelectionParams(
    language_code="yo-NG",  # Yoruba (Nigeria)
    name="yo-NG-Standard-A"
)
```

---

### Issue: User Speaks Mixed Languages

**Symptom:** User switches between English and local language mid-conversation

**Solution:** This is actually handled automatically!
- Whisper auto-detects language per utterance
- GPT-4o can understand code-switching
- Agent responds appropriately

**Example:**
```
User: "Send 50 to John for dinner" (English)
Agent: "£50 to John. Confirm?" (English)
User: "Ee" (Igbo for "Yes")
Agent: "Done!" (English - continues in current language)
```

---

### Issue: Low STT Accuracy

**Symptom:** Voice agent doesn't understand user correctly

**Solutions:**
1. **Check audio quality**: Ensure good microphone and low background noise
2. **Use language hints**: Metadata language helps Whisper focus
3. **Prompt user to speak clearly**: Add UI guidance
4. **Fallback to text**: Offer text input as backup

---

## Future Enhancements

### Planned Features

1. **More Nigerian Languages**
   - Add Edo, Fulani, Kanuri
   - Regional dialect support

2. **Improved TTS**
   - Integrate Google Cloud TTS for native voices
   - Custom voice models for better pronunciation

3. **Language Switching**
   - Allow mid-conversation language changes
   - "Switch to Yoruba" voice command

4. **Offline Mode**
   - Download language models for offline use
   - Basic transactions without internet

5. **Voice Biometrics**
   - Language-agnostic voice authentication
   - Enhanced security across all languages

6. **SMS Fallback**
   - Send transaction confirmations via SMS in user's language
   - Useful for poor internet connections

---

## Best Practices

### For Developers

1. **Always pass language in metadata**
   ```dart
   metadata: {'language': userPreferredLanguage}
   ```

2. **Log language selection**
   ```python
   logger.info(f"User language: {language.value}")
   ```

3. **Test all 4 languages regularly**
   - English: Daily
   - Igbo/Hausa/Yoruba: Weekly minimum

4. **Monitor error rates by language**
   - Track which languages have higher failure rates
   - Improve prompts accordingly

5. **Provide language-specific help**
   - UI instructions in each language
   - Example phrases users can say

### For Users

1. **Set your preferred language in app settings**
2. **Speak clearly and at normal pace**
3. **Use natural phrases** (the AI understands context)
4. **Mix languages if comfortable** (code-switching is supported)
5. **Provide feedback** if pronunciations are unclear

---

## Examples in All Languages

### Send Money - All Languages

**English:**
```
User: "Send 100 to Sarah"
Agent: "£100 to Sarah. Confirm?"
User: "Yes"
Agent: "Done!"
```

**Igbo:**
```
Onye ọrụ: "Zie 100 nye Sarah"
Agent: "100 nye Sarah. Kwenye?"
Onye ọrụ: "Ee"
Agent: "Emechara!"
```

**Hausa:**
```
Mai amfani: "Aika 100 zuwa Sarah"
Agent: "100 zuwa Sarah. Tabbatar?"
Mai amfani: "I"
Agent: "An gama!"
```

**Yoruba:**
```
Olùmúlò: "Fi 100 ranṣẹ́ sí Sarah"
Agent: "100 sí Sarah. Jẹ́rìísí?"
Olùmúlò: "Bẹẹni"
Agent: "Ti parí!"
```

---

### Error Handling - All Languages

**English:**
```
Agent: "Can't find Sarah. Spell it?"
User: "S-A-R-A-H J-O-H-N-S-O-N"
```

**Igbo:**
```
Agent: "Ahụghị m Sarah. Sụpee ya?"
Onye ọrụ: "S-A-R-A-H J-O-H-N-S-O-N"
```

**Hausa:**
```
Agent: "Ban same Sarah ba. Rubuta shi?"
Mai amfani: "S-A-R-A-H J-O-H-N-S-O-N"
```

**Yoruba:**
```
Agent: "Mi ò rí Sarah. Ṣe ìsípẹ́lì rẹ̀?"
Olùmúlò: "S-A-R-A-H J-O-H-N-S-O-N"
```

---

## Conclusion

LazerVault's multilingual voice banking makes financial services accessible to millions of Nigerians in their native languages. With support for English, Igbo, Hausa, and Yoruba, users can now bank using voice commands in the language they're most comfortable with.

### Key Benefits:
✅ **Accessibility**: Banking for non-English speakers
✅ **Speed**: Fast transactions in any language (3-5 turns)
✅ **Natural**: Speak as you normally would
✅ **Inclusive**: Supports Nigeria's major languages
✅ **Smart**: Auto-detects language, understands code-switching

---

**Version:** 1.0
**Last Updated:** November 17, 2025
**Supported Languages:** English, Igbo, Hausa, Yoruba
**Status:** ✅ Production Ready
