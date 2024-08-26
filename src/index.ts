import { GetData } from './lib/GetData';
import fs from 'fs';
import path from 'path';
import { DataType } from './types/DataType';

const dataPath = path.resolve(__dirname, '../assets/data.json');
const data = JSON.parse(fs.readFileSync(dataPath, 'utf8'));

// GetData("https://myweb.cmu.ac.th/sansanee.a/IntroCI/dataset/Flood_dataset.txt");

console.log(data);