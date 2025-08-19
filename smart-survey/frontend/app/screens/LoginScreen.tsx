import React, { useState } from 'react';
import { View, Text, TextInput, Button } from 'react-native';
import API from '../lib/api';
import * as SecureStore from 'expo-secure-store';

export default function LoginScreen({ navigation }: any){
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const login = async ()=>{
    setLoading(true);
    try{
      const res = await API.post('/auth/login', { email, password });
      const token = res.data.token;
      await SecureStore.setItemAsync('jwt', token);
      navigation.replace('SurveyPicker');
    }catch(err:any){
      alert(err?.response?.data?.error?.message || 'Login failed');
    }finally{ setLoading(false) }
  };

  return (
    <View style={{flex:1, padding:12}}>
      <Text style={{fontSize:20}}>Login</Text>
      <TextInput placeholder="Email" value={email} onChangeText={setEmail} style={{borderWidth:1, padding:8, marginTop:8}} />
      <TextInput placeholder="Password" value={password} onChangeText={setPassword} secureTextEntry style={{borderWidth:1, padding:8, marginTop:8}} />
      <Button title={loading ? 'Logging...' : 'Login'} onPress={login} />
      <View style={{height:12}} />
      <Button title="Signup" onPress={()=>navigation.navigate('Signup')} />
    </View>
  );
}
