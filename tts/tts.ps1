Param(
    [Parameter(Position=0, mandatory=$true)]
    [string] $TextToSay
)

Function Main {
    Add-Type -AssemblyName System.Speech
    (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak($TextToSay)
}

Main
