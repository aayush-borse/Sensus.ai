import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import LoginScreen from './app/screens/LoginScreen';
import SignupScreen from './app/screens/SignupScreen';
import SurveyPicker from './app/screens/SurveyPicker';
import ChatSurvey from './app/screens/ChatSurvey';
import ThankYou from './app/screens/ThankYou';
import AdminDashboard from './app/screens/AdminDashboard';

const Stack = createNativeStackNavigator();

export default function App(){
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Login">
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="Signup" component={SignupScreen} />
        <Stack.Screen name="SurveyPicker" component={SurveyPicker} />
        <Stack.Screen name="ChatSurvey" component={ChatSurvey} />
        <Stack.Screen name="ThankYou" component={ThankYou} />
        <Stack.Screen name="Admin" component={AdminDashboard} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
