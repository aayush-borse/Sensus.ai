import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, Button, FlatList } from 'react-native';
import API from '../lib/api';
import * as Location from 'expo-location';

export default function ChatSurvey({ route, navigation }: any) {
  const surveyId = route?.params?.surveyId || 'svy_123';
  const [questions, setQuestions] = useState<any[]>([]);
  const [answers, setAnswers] = useState<any[]>([]);
  const [deviceId] = useState('dev-' + Math.random().toString(36).slice(2,9));
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    API.get(`/survey/questions?surveyId=${surveyId}&lang=en`).then(r => setQuestions(r.data.questions)).catch(()=>{});
  }, []);

  const submit = async () => {
    setLoading(true);
    try{
      const loc = await Location.getCurrentPositionAsync({});
      const payload = {
        surveyId,
        deviceId,
        language: 'en',
        answers,
        location: { lat: loc.coords.latitude, lng: loc.coords.longitude, accuracy: loc.coords.accuracy, timestamp: Math.floor(Date.now()/1000) },
        completionTimeSeconds: 60
      };
      const res = await API.post('/survey/submit', payload);
      navigation.navigate('ThankYou', { responseId: res.data.responseId });
    }catch(err:any){
      alert(err?.response?.data?.error?.message || 'Submit failed');
    }finally{ setLoading(false) }
  };

  return (
    <View style={{flex:1, padding:12}}>
      <Text style={{fontSize:18, marginBottom:8}}>Chat Survey (demo)</Text>
      <FlatList
        data={questions}
        keyExtractor={(i:any) => i.id}
        renderItem={({item}) => (
          <View style={{marginVertical:8}}>
            <Text>{item.prompt}</Text>
            <TextInput onChangeText={(t)=>{ const idx = answers.findIndex(a=>a.questionId===item.id); if(idx>=0){answers[idx].value = t; setAnswers([...answers])} else {setAnswers([...answers, {questionId:item.id, value:t}])}}} style={{borderWidth:1, padding:8}} />
          </View>
        )}
      />
      <Button title={loading ? 'Sending...' : 'Submit'} onPress={submit} />
    </View>
  );
}
