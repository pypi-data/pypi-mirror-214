import os
import re
import json5
import datetime
import itertools
import subprocess

from pathlib import Path
from filehash import FileHash
from argparse import ArgumentParser
from multiprocessing import Pool


class _Cons:
	iDiPa: Path
	oDiPa: Path

	exifRules: dict
	typeLogos: dict

	################################################################

	def __init__(self):
		parser = ArgumentParser()
		parser.add_argument('i', type=Path)
		parser.add_argument('o', type=Path)
		args = parser.parse_args()

		self.iDiPa = args.i.absolute()
		self.oDiPa = args.o.absolute()

		assert self.iDiPa.is_dir()
		assert not self.oDiPa.exists()

		################################################################

		self.exifRules = {
			'Type': ['FileType'],
			'Extension': ['FileTypeExtension'],
			'Brand': [
				'Make',
				# 'HandlerVendorID',
			],
			'Model': ['Model'],
			'Moment': [
				"SubSecCreateDate",
				# "SubSecDateTimeOriginal",
				"MediaCreateDate",
				"DateTimeOriginal",
				"ModifyDate",
				"FileModifyDate",
			],
		}

		self.typeLogos = {
			'BMP': '📸',
			'DNG': '📸',
			'JPEG': '📸',
			'MKA': '🎤',
			'MOV': '📹',
			'M4A': '🎤',
			'MP3': '🎤',
			'MP4': '📹',
			'PNG': '📸',
			'WAV': '🎤',
			'': '❔',
		}

		pass

	pass


################################################################

def _genTypePart(t: str, typeLogos: dict):
	if t in typeLogos:
		logo = typeLogos[t]
		return '｜'.join([logo, t])
		pass
	else:
		print('Unknown Type:', t)
		pass
	pass


def _genDevicePart(brand: str, model: str):
	return '｜'.join([_.replace(' ', '-') for _ in [brand, model]])


def _genMomentPart(val: str, lev: int):
	val = val.replace('::', ':')
	head = val[:19]
	tail = val[19:]

	dt = datetime.datetime.strptime(head, '%Y:%m:%d %H:%M:%S')
	delta = re.search('[+-]\d+:\d+', tail)
	if delta:
		delta = delta.group(0)
		sign = {'+': -1, '-': 1}[delta[0]]
		h = int(delta[1:3])
		m = int(delta[4:6])
		delta = sign * datetime.timedelta(hours=h, minutes=m)
		dt += delta
		pass

	ms = re.search('\.\d+', tail)
	ms = ms.group(0)[1:4] if ms else '~~~'

	__date = dt.strftime('%Y-%m-%d')
	__time = dt.strftime('%H`%M`%S,') + ms
	__level = chr(9312 + lev)

	return '｜'.join([__date, __time, __level])


def _genFiPa(tFiPa: Path, _CONS: _Cons):
	cmd = 'ExifTool -j "%s"' % tFiPa
	proc = subprocess.run(cmd, stdout=subprocess.PIPE, check=False, encoding='UTF-8')
	exif = json5.loads(proc.stdout)[0]

	keyInfo = dict()
	for field, rule in _CONS.exifRules.items():
		value = ''
		level = None
		for lev, tag in enumerate(rule):
			if tag in exif:
				val = str(exif[tag])
				if not val.startswith('0000'):
					value = val
					level = lev
					break
				pass
			pass
		keyInfo[field] = (value, level)
		pass

	typePart = _genTypePart(keyInfo['Type'][0], _CONS.typeLogos)
	devicePart = _genDevicePart(keyInfo['Brand'][0], keyInfo['Model'][0])
	momentPart = _genMomentPart(*keyInfo['Moment'])
	ext = keyInfo['Extension'][0]

	fn = (momentPart + '.' + ext) if ext else momentPart
	destFiPa: Path = _CONS.oDiPa / typePart / devicePart / fn

	return destFiPa


def _genMeta(iFiPa: Path, tFiPa: Path, _CONS: _Cons):
	modify: float = os.path.getmtime(iFiPa)

	iFiPa.rename(tFiPa)
	destFiPa: Path = _genFiPa(tFiPa, _CONS)
	tFiPa.rename(iFiPa)

	hCode: str = FileHash('sha1').hash_file(iFiPa)

	meta = (
		hCode,
		modify,
		destFiPa,
		iFiPa,
	)
	return meta


################################################################

def _analyze(metas: list[tuple[str, float, Path, Path]]):
	quads = sorted(metas)
	quadGroups = [tuple(_[1]) for _ in itertools.groupby(quads, lambda _: _[0])]

	pairs = sorted([list(_[0])[2:] for _ in quadGroups])
	pairGroups: list[tuple[Path, Path]] = [tuple(_[1]) for _ in itertools.groupby(pairs, lambda _: _[0])]

	tasks = list()
	for group in pairGroups:
		for idx, (destFiPa, iFiPa) in enumerate(group):
			oFiPa = destFiPa.with_stem('%s｜%d' % (destFiPa.stem, idx + 1))
			tasks.append((iFiPa, oFiPa))
			pass
		pass
	return tasks


################################################################

def _main():
	iFiPas = [Path(_[0]) / fn for _ in os.walk(_CONS.iDiPa) for fn in _[2]]

	L = len(iFiPas)
	cons = [_CONS] * L
	fmt = '{:0>%d}' % len(str(L - 1))
	tDiPa = _CONS.oDiPa
	tFiPas = [tDiPa / fmt.format(_) for _ in range(L)]

	args = list(zip(iFiPas, tFiPas, cons))
	tDiPa.mkdir(parents=True)
	with Pool() as pool:
		metas = pool.starmap(_genMeta, args)
		pass

	tasks: list[tuple[Path, Path]] = _analyze(metas)

	for iFiPa, oFiPa in tasks:
		oFiPa.parent.mkdir(parents=True, exist_ok=True)
		iFiPa.rename(oFiPa)
		pass

	pass


if __name__ == '__main__':
	_CONS = _Cons()
	_main()
	pass
