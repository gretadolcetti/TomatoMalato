# TomatoMalato
ML web and mobile app for tomato diseases prediction.

## Start web app
From project root
```
cd tomato_malato_web
flask --app home.py run
```

## Start mobile app on emulator
From project root
```
cd tomato_malato_app
flutter emulators # To list all the available emulators
flutter emulators --launch $CHOSEN_EMULATOR_NAME
flutter run --no-sound-null-safety
```